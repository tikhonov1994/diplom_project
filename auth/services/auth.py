import hashlib
import time
from datetime import timedelta

from db.storage import UserInfoStorageDep, AuthDep, UserRoleStorageDep, UserSessionStorageDep, ItemNotFoundException, DbConflictException
from passlib.context import CryptContext
from db.redis_db import RedisDep
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy import select
from db.model import UserInfo, UserSession
from schemas.auth import TokensSchema
from core.config import app_config
import logging


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging.basicConfig(filename='logging.log', level=int(20),
                    format='%(asctime)s  %(message)s')
logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self,
                 user_info_storage: UserInfoStorageDep,
                 user_session_storage: UserSessionStorageDep,
                 role_storage: UserRoleStorageDep,
                 redis: RedisDep,
                 Authorize: AuthDep
                 ) -> None:
        self._user_info_storage = user_info_storage
        self._user_session_storage = user_session_storage
        self._role_storage = role_storage
        self.redis = redis
        self.Authorize = Authorize

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
        user_session = UserSession(id=token_jti,user_info_id=user.id, refresh_token=tokens.refresh_token, user_agent=user_agent)
        await self._user_session_storage.add_session(user_session)

        return tokens

    async def refresh(self, refresh_token: str, user_agent: str) -> TokensSchema:
        try:
            await self.Authorize._verify_jwt_in_request(token=refresh_token, type_token='refresh', token_from='headers')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        refresh_token_data = await self.Authorize.get_raw_jwt(refresh_token)
        if not refresh_token_data['sub']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')

        token_jti = await self.Authorize.get_jti(refresh_token)

        # удалить из БД если время истекло
        if refresh_token_data['exp'] < time.time():
            await self._user_session_storage.generic.delete(token_jti)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )

        user = await self._user_info_storage.generic.get(refresh_token_data['sub'])
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')

        current_session = await self._user_session_storage.generic.get(token_jti)
        if not current_session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')

        # удалить из БД сессию если время истекло
        if refresh_token_data['exp'] < time.time():
            await self._user_session_storage.generic.delete(token_jti)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )

        user_role = await self._role_storage.generic.get(user.user_role_id)
        claims = {
            'email': user.email,
            'role': user_role.name,
            'user_agent': user_agent,
        }
        tokens = await self._create_tokens(user, claims)

        # обновляем в БД рефреш токен на новый
        self._user_session_storage.update_refresh_token(current_session.id, tokens.refresh_token)

        return tokens


    @staticmethod
    async def check_password(pass_to_check: str, user: UserInfo):
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

    async def _create_tokens(self, user, claims) -> TokensSchema:
        access_token = await self.Authorize.create_access_token(
            subject=str(user.id),
            expires_time=timedelta(minutes=app_config.auth_token_expire_minutes),
            user_claims=claims
        )

        refresh_token = await self.Authorize.create_refresh_token(
            subject=str(user.id),
            expires_time=timedelta(minutes=app_config.refresh_token_expire_minutes),
        )

        return TokensSchema(access_token=access_token, refresh_token=refresh_token)