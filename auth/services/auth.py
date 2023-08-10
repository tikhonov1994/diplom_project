import hashlib
from datetime import timedelta

from db.storage import UserInfoStorageDep, AuthDep, UserRoleStorageDep, UserSessionStorageDep, ItemNotFoundException, DbConflictException
from fastapi import HTTPException, status
from sqlalchemy import select
from db.model import UserInfo, UserSession
from schemas.auth import TokensSchema
from core.config import app_config
import logging

logging.basicConfig(filename='logging.log', level=int(20),
                    format='%(asctime)s  %(message)s')
logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self,
                 user_info_storage: UserInfoStorageDep,
                 user_session_storage: UserSessionStorageDep,
                 role_storage: UserRoleStorageDep,
                 Authorize: AuthDep
                 ) -> None:
        self._user_info_storage = user_info_storage
        self._user_session_storage = user_session_storage
        self._role_storage = role_storage
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
        user_session = UserSession(id=token_jti, user_info_id=user.id, refresh_token=tokens.refresh_token, user_agent=user_agent)
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