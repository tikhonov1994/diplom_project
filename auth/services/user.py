from fastapi import HTTPException
from starlette import status

from db.model import UserInfo
from db.storage.generic_storage import GenericStorageException
from uuid import UUID

from db.storage import UserInfoStorageDep, UserRoleStorageDep, ItemNotFoundException
from services.exceptions import ServiceItemNotFound
from schemas.user import UserInfoSchema
from services.utils import generate_hashed_password

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
        raise UserEmailNotFoundException(email=email)

    async def check_user_by_email(self, email: str) -> bool:
        stmt = select(UserInfo).where(UserInfo.email == email)
        if (await self._user_info_storage.generic._session.execute(stmt)).first():
            return True
        return False
    
    async def save_user(self, email: str, password: str):
        if await self.check_user_by_email(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User with email {email} already exists!')
        hashed_password = generate_hashed_password(password)
        role = await self._role_storage.get_default_role()
        user = UserInfo(email=email, password_hash=hashed_password, user_role_id=role.id)
        await self._user_info_storage.add_user(user)
