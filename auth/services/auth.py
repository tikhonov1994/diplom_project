import hashlib
from datetime import timedelta

from db.storage import UserInfoStorageDep, AuthDep, UserRoleStorageDep, UserSessionStorageDep, ItemNotFoundException, DbConflictException
from passlib.context import CryptContext
from db.redis_db import RedisDep
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy import select
from db.model import UserInfo, UserSession
from schemas.auth import TokensSchema
from core.config import app_config
from services.utils import UtilService
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

        # user_role = await self._role_storage.generic.get(user.user_role_id)[0].name
        user_role = await self._role_storage.generic.get(user.user_role_id)

        user_claims = {
            'email': email,
            'role': user_role.name,
            'user_agent': user_agent,
        }
        tokens = await self.create_tokens(user, user_claims)

        user_session = UserSession(user_info_id=user.id, refresh_token=tokens.refresh_token, session_type='wqe')
        await self._user_session_storage.add_session(user_session)

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
            if not await self.check_password(password, user[0]):
                return False

            return user[0]

        return False

    async def create_tokens(self, user, user_claims) -> TokensSchema:
        access_token = await self.Authorize.create_access_token(
            subject=str(user.id),
            expires_time=timedelta(minutes=app_config.auth_token_expire_minutes),
            user_claims=user_claims
        )

        refresh_token = await self.Authorize.create_refresh_token(
            subject=str(user.id),
            expires_time=timedelta(minutes=app_config.refresh_token_expire_minutes),
        )

        return TokensSchema(access_token=access_token, refresh_token=refresh_token)