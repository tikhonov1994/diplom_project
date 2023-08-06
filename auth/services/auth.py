from datetime import timedelta

from db.storage import UserInfoStorageDep, AuthDep, UserRoleStorageDep, UserSessionStorageDep, ItemNotFoundException, DbConflictException
from passlib.context import CryptContext
from db.redis_db import RedisDep
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy import select
from db.model import UserInfo
from schemas.auth import Tokens

# from services import UserServiceDep

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class AuthService:
    def __init__(self,
                 user_info_storage: UserInfoStorageDep,
                 user_session_storage: UserSessionStorageDep,
                 role_storage: UserRoleStorageDep,
                 # user_service: UserServiceDep,
                 redis: RedisDep,
                 Authorize: AuthDep
                 ) -> None:
        self._user_info_storage = user_info_storage
        # self.user_service = user_service
        self._user_session_storage = user_session_storage
        self._role_storage = role_storage
        self.redis = redis
        self.Authorize = Authorize

    async def login(self, email: str, password: str) -> Tokens:
        user = await self.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        # user_role = await self._role_storage.get(user.user_role_id)

        # todo
        # self._user_session_storage.add_session()

        user_claims = {
            'email': email,
            # 'role': user_role,
            # 'user_agent': request.user_agent,
        }
        tokens = await self.create_tokens(user, user_claims)

        # self.redis.set(
        #     name=str(user.id),
        #     value=tokens.refresh_token,
        #     ex=timedelta(minutes=config.refresh_token_expire_minutes),
        # )

        return tokens
        # return {'status': 'success', 'access_token': access_token}

    async def authenticate_user(self, email: str, password: str) -> UserInfo:
        stmt = select(UserInfo).where(UserInfo.email == email)
        if user := (await self._user_info_storage.generic._session.execute(stmt)).first():
            if not await self.verify_password(password, user.password_hash):
                return False

            return user

        return False

    # async def create_tokens(self, user, user_claims) -> Tokens:
    #     access_token = await self.Authorize.create_access_token(
    #         subject=str(user.id),
    #         expires_time=timedelta(minutes=config.auth_token_expire_minutes),
    #         user_claims=user_claims
    #     )
    #
    #     refresh_token = await self.Authorize.create_refresh_token(
    #         subject=str(user.id),
    #         expires_time=timedelta(minutes=config.refresh_token_expire_minutes),
    #     )
    #
    #     return Tokens(access_token=access_token, refresh_token=refresh_token)
        # return str(access_token), str(refresh_token)

    async def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)