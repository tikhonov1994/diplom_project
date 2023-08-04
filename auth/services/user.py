import os
import hashlib

from typing import Annotated

from fastapi import Depends
from db.model import UserInfo
from db.storage import UserInfoStorageDep
from db.storage.generic_storage import GenericStorageException
from uuid import UUID

from db.storage import UserInfoStorageDep, UserRoleStorageDep, ItemNotFoundException
from services.exceptions import ServiceItemNotFound
from schemas.user import UserInfoSchema

from sqlalchemy import select


class UserEmailNotFoundException(GenericStorageException):
    def __init__(self, email: str) -> None:
        super().__init__()
        self._instance_email = email

    def __repr__(self) -> str:
        return f'User with email: \'{self._instance_email}\' not found'


class UserService:

    def __init__(self,
                 user_info_storage: UserInfoStorageDep,
                 role_storage: UserRoleStorageDep) -> None:
        self._user_info_storage = user_info_storage
        self._role_storage = role_storage

    async def get_user_info(self, user_id: UUID) -> UserInfoSchema:
        if user_info := await self._user_info_storage.generic.get(user_id):
            return UserInfoSchema.from_orm(user_info)
        raise ServiceItemNotFound(item_name='UserInfo', item_id=user_id)

    async def grant_role_to_user(self, user_id: UUID, role_id: UUID) -> None:
        try:
            role = await self._role_storage.generic.get(role_id)
            await self._user_info_storage.update_user_role(user_id, role)
        except ItemNotFoundException as exc:
            raise ServiceItemNotFound(item_name=exc.type_name, item_id=exc.item_id)

    async def get_user_by_email(self, email: str) -> UserInfo:
        stmt = select(UserInfo).where(UserInfo.email == email)
        if result := (await self._user_info_storage.generic._session.execute(stmt)).first():
            return result
        raise UserEmailNotFoundException(item_type=UserInfo, email=email)

    async def check_user_by_email(self, email: str) -> bool:
        stmt = select(UserInfo).where(UserInfo.email == email)
        if (await self._user_info_storage.generic._session.execute(stmt)).first():
            return True
        return False

    @staticmethod
    async def generate_hashed_password(password: str):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        return key + salt

    @staticmethod
    async def check_password(pass_to_check: str, user: UserInfo):
        password = user.password_hash
        salt = password[-32:]
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            pass_to_check.encode('utf-8'), # Конвертирование пароля в байты
            salt, 
            100000
        )
        if new_key == password:
            return True
        else:
            return False
    
    async def save_user(self, email: str, hashed_password: str):
        user = UserInfo(email=email, password_hash=hashed_password)
        await self._user_info_storage.add_user(user)


UserServiceDep = Annotated[UserService, Depends()]
