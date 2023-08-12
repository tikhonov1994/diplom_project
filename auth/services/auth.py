import hashlib
import time
import datetime as dt

from db.storage import (UserInfoStorageDep, AuthDep, UserRoleStorageDep, UserSessionStorageDep,
                        ItemNotFoundException, DbConflictException, RedisDep)
from fastapi import HTTPException, status
from sqlalchemy import select
from db.model import UserInfo, UserSession
from schemas.auth import TokensSchema
from core.config import app_config

import logging
from async_fastapi_jwt_auth.exceptions import JWTDecodeError

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

        token_jti = await self.Authorize.get_jti(tokens.refresh_token)
        user_session = UserSession(id=token_jti, user_info_id=user.id, refresh_token=tokens.refresh_token,
                                   user_agent=user_agent, refresh_token_jti=token_jti, start_at=dt.datetime.now())
        await self._user_session_storage.add_session(user_session)

        return tokens

    @staticmethod
    async def check_password(pass_to_check: str, user: UserInfo):
        # FIXME
        password = user.password_hash.decode('utf-8')
        salt = password[-32:]
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            pass_to_check.encode('utf-8'), # Конвертирование пароля в байты
            salt,
            100000
        )

        if (new_key + salt) == password:
            return True
        else:
            return False

    async def authenticate_user(self, email: str, password: str) -> UserInfo:
        stmt = select(UserInfo).where(UserInfo.email == email)
        if user := (await self._user_info_storage.generic._session.execute(stmt)).first():
            # fixme
            # if not await self.check_password(password, user[0]):
            #     return False

            return user[0]

        return False

    async def get_session_by_jti(self, refresh_jti: str):
        stmt = select(UserSession).where(UserSession.refresh_token_jti == refresh_jti)
        if user_session := (await self._user_session_storage.generic._session.execute(stmt)).first():
            return user_session[0]
        raise ItemNotFoundException(UserSession, user_session)

    async def _create_tokens(self, user, claims) -> TokensSchema:
        access_token = await self.Authorize.create_access_token(
            subject=str(user.id),
            expires_time=dt.timedelta(minutes=app_config.auth_token_expire_minutes),
            user_claims=claims
        )

        refresh_token = await self.Authorize.create_refresh_token(
            subject=str(user.id),
            expires_time=dt.timedelta(minutes=app_config.refresh_token_expire_minutes),
        )

        return TokensSchema(access_token=access_token, refresh_token=refresh_token)

    async def close_session(self, user_session: UserSession):
        await self._user_session_storage.close_session(user_session)

    async def logout(self):
        try:
            await self.Authorize.jwt_required()
        except JWTDecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')
        decrypted_token = await self.Authorize.get_raw_jwt()
        jti = decrypted_token['jti']
        refresh_jti = decrypted_token['refresh_jti']
        user_session = await self.get_session_by_jti(refresh_jti)
        refresh_exp = (await self.Authorize.get_raw_jwt(user_session.refresh_token))['exp']
        self.redis.setex(jti, (decrypted_token['exp'] - int(time.time())), 'true')
        self.redis.setex(refresh_jti, (refresh_exp - int(time.time())), 'true')
        await self.close_session(user_session)
