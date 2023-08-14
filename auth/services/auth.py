import datetime
import hashlib
import time
import datetime as dt
from uuid import UUID

from async_fastapi_jwt_auth.exceptions import JWTDecodeError
from db.storage import (UserInfoStorageDep, AuthDep, UserRoleStorageDep, UserSessionStorageDep,
                        ItemNotFoundException, DbConflictException)
from db.redis import RedisDep
from fastapi import HTTPException, status
from sqlalchemy import select
from db.model import UserInfo, UserSession
from schemas.auth import TokensSchema
from core.config import app_config
from services.utils import check_password


import logging

logging.basicConfig(filename='logging.log', level=int(20),
                    format='%(asctime)s  %(message)s')
logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self,
                 user_info_storage: UserInfoStorageDep,
                 user_session_storage: UserSessionStorageDep,
                 role_storage: UserRoleStorageDep,
                 Authorize: AuthDep,
                 # redis: RedisDep,
                 ) -> None:
        self._user_info_storage = user_info_storage
        self._user_session_storage = user_session_storage
        self._role_storage = role_storage
        self.Authorize = Authorize
        # self.redis = redis

    async def login(self, email: str, password: str, user_agent: str) -> TokensSchema:
        user = await self.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        user_role = await self._role_storage.generic.get(user.user_role_id)
        claims = {
            'email': email,
            'role': user_role.name,
            'user_agent': user_agent,
        }
        tokens = await self._create_tokens(user, claims)

        new_access_token_data = await self.Authorize.get_raw_jwt(tokens.access_token)
        expire_time = datetime.datetime.fromtimestamp(new_access_token_data['exp'])
        refresh_token_jti = await self.Authorize.get_jti(tokens.refresh_token)

        user_session = UserSession(user_info_id=user.id, user_agent=user_agent, refresh_token_jti=refresh_token_jti, start_at=dt.datetime.now(), end_at=expire_time)

        await self._user_session_storage.add_session(user_session)

        return tokens

    async def refresh(self, refresh_token: str, user_agent: str) -> TokensSchema:
        try:
            # используется protected метод т.к. публичный требует чтобы токен был в хедерах/куках
            await self.Authorize._verify_jwt_in_request(token=refresh_token, type_token='refresh', token_from='headers')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        refresh_token_data = await self.Authorize.get_raw_jwt(refresh_token)
        if not refresh_token_data['sub']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')

        if refresh_token_data['exp'] < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
            )

        user = await self._user_info_storage.generic.get(refresh_token_data['sub'])
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token not exist')

        current_session = await self._user_session_storage.get_session_by_refresh_token(refresh_token_data['jti'])
        if not current_session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')

        user_role = await self._role_storage.generic.get(user.user_role_id)
        claims = {
            'email': user.email,
            'role': user_role.name,
            'user_agent': user_agent,
        }
        tokens = await self._create_tokens(user, claims)

        new_access_token_data = await self.Authorize.get_raw_jwt(tokens.access_token)
        expire_time = datetime.datetime.fromtimestamp(new_access_token_data['exp'])
        refresh_token_jti = await self.Authorize.get_jti(tokens.refresh_token)
        await self._user_session_storage.refresh_session(current_session.id, refresh_token_jti, expire_time)

        return tokens

    async def authenticate_user(self, email: str, password: str) -> UserInfo:
        stmt = select(UserInfo).where(UserInfo.email == email)
        if user := (await self._user_info_storage.generic._session.execute(stmt)).first():
            # FIXME не работает
            # if not await check_password(password, user[0]):
            #     return False

            return user[0]

        return False

    async def get_session_by_jti(self, refresh_jti: str):
        stmt = select(UserSession).where(UserSession.refresh_token_jti == refresh_jti)
        if user_session := (await self._user_session_storage.generic._session.execute(stmt)).first():
            return user_session[0]
        raise ItemNotFoundException(UserSession, user_session)

    async def _create_tokens(self, user, claims) -> TokensSchema:
        refresh_token = await self.Authorize.create_refresh_token(
            subject=str(user.id),
            expires_time=dt.timedelta(minutes=app_config.refresh_token_expire_minutes),
        )
        claims["refresh_jti"] = await self.Authorize.get_jti(refresh_token)

        access_token = await self.Authorize.create_access_token(
            subject=str(user.id),
            expires_time=dt.timedelta(minutes=app_config.auth_token_expire_minutes),
            user_claims=claims
        )

        return TokensSchema(access_token=access_token, refresh_token=refresh_token)

    async def close_session(self, user_session: UserSession):
        await self._user_session_storage.close_session(user_session)

    async def logout(self):
        await self.get_token()
        decrypted_token = await self.Authorize.get_raw_jwt()
        jti = decrypted_token['jti']
        refresh_jti = decrypted_token['refresh_jti']
        user_session = await self.get_session_by_jti(refresh_jti)
        refresh_exp = (await self.Authorize.get_raw_jwt(user_session.refresh_token))['exp']
        # self.redis.setex(jti, (decrypted_token['exp'] - int(time.time())), 'true')
        # self.redis.setex(refresh_jti, (refresh_exp - int(time.time())), 'true')
        await self.close_session(user_session)

    async def get_token(self):
        try:
            await self.Authorize.jwt_required()
        except JWTDecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')

    async def get_user_history(self, user_id: int):
        stmt = select(UserSession).where(UserSession.user_info_id == user_id)
        if sessions := await self._user_info_storage.generic._session.execute(stmt):
            res = []
            for i in sessions:
                res.append({
                    'session_started': i[0].start_at,
                    'session_ended': i[0].end_at,
                    'user_agent': i[0].user_agent
                })
            print(res)
            return res
        return None
