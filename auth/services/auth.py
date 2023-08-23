import datetime as dt
import logging
import time
from uuid import UUID

from async_fastapi_jwt_auth.exceptions import JWTDecodeError
from core.config import app_config
from db.model import UserInfo, UserSession
from db.redis import RedisDep
from db.storage import (AuthDep, ItemNotFoundException,
                        UserEmailNotFoundException, UserInfoStorageDep,
                        UserRoleStorageDep, UserSessionStorageDep)
from fastapi import HTTPException, status
from schemas.auth import TokensSchema, LoginResponseSchema
from services.utils import check_password
from sqlalchemy import select

logging.basicConfig(filename='logging.log', level=int(20),
                    format='%(asctime)s  %(message)s')
logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self,
                 user_info_storage: UserInfoStorageDep,
                 user_session_storage: UserSessionStorageDep,
                 role_storage: UserRoleStorageDep,
                 Authorize: AuthDep,
                 redis: RedisDep,
                 ) -> None:
        self._user_info_storage = user_info_storage
        self._user_session_storage = user_session_storage
        self._role_storage = role_storage
        self.Authorize = Authorize
        self.redis = redis

    async def login_by_password(self, email: str, password: str, user_agent: str) -> TokensSchema:
        user = await self.authenticate_user(email, password)
        return await self.login(user, user_agent)

    async def login(self, user: UserInfo, user_agent: str) -> TokensSchema:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        claims = {
            'email': user.email,
            'role': user.role.name,
            'user_agent': user_agent,
        }
        tokens = await self._create_tokens(user, claims)

        new_access_token_data = await self.Authorize.get_raw_jwt(tokens.access_token)
        expire_time = dt.datetime.fromtimestamp(new_access_token_data['exp'])
        refresh_token_jti = await self.Authorize.get_jti(tokens.refresh_token)

        user_session = UserSession(user_info_id=user.id, user_agent=user_agent, refresh_token_jti=refresh_token_jti,
                                   start_at=dt.datetime.now(), end_at=expire_time)

        await self._user_session_storage.add_session(user_session)

        result = LoginResponseSchema(access_token=tokens.access_token, refresh_token=tokens.refresh_token,
                                     user_id=user.id, email=user.email, role=user.role.name)

        return result

    async def refresh(self, refresh_token: str, user_agent: str) -> TokensSchema:
        try:
            # используется protected метод т.к. публичный требует чтобы токен был в хедерах/куках
            await self.Authorize._verify_jwt_in_request(token=refresh_token, type_token='refresh', token_from='headers')
        except Exception:
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
        expire_time = dt.datetime.fromtimestamp(new_access_token_data['exp'])
        refresh_token_jti = await self.Authorize.get_jti(tokens.refresh_token)
        await self._user_session_storage.refresh_session(current_session.id, refresh_token_jti, expire_time)

        return tokens

    async def authenticate_user(self, email: str, password: str) -> UserInfo | None:
        try:
            user = await self._user_info_storage.get_user_by_email(email)
            if check_password(password, user):
                return user
        except UserEmailNotFoundException:
            return False
        return None

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
        await self.redis.setex(jti, (decrypted_token['exp'] - int(time.time())), 'true')
        await self.redis.setex(refresh_jti, (int(user_session.end_at.timestamp()) - int(time.time())), 'true')
        await self.close_session(user_session)

    async def get_token(self):
        try:
            await self.Authorize.jwt_required()
        except JWTDecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')

    async def get_user_id(self) -> UUID:
        await self.get_token()
        return UUID(await self.Authorize.get_jwt_subject())

    async def get_user_history(self):
        user_id = await self.get_user_id()
        stmt = select(UserSession).where(UserSession.user_info_id == user_id)
        if sessions := await self._user_info_storage.generic._session.execute(stmt):
            res = {'results': []}
            for i in sessions:
                res['results'].append({
                    'session_started': i[0].start_at,
                    'session_ended': i[0].end_at,
                    'user_agent': i[0].user_agent
                })
            res['count'] = len(res['results'])
            return res
        return None

    async def get_user_id(self):
        await self.get_token()
        return await self.Authorize.get_jwt_subject()
