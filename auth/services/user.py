from uuid import UUID

from db.model import UserInfo
from db.storage import (ItemNotFoundException, UserInfoStorageDep,
                        UserRoleStorageDep)
from schemas.user import PatchUserInfoSchema, UserInfoSchema
from services.exceptions import (ServiceItemNotFound,
                                 ServiceItemSearchException,
                                 ServiceUniqueFieldViolation)
from services.utils import generate_hashed_password


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

    async def get_user_info_by_email(self, email: str) -> UserInfoSchema:
        if user_info := await self._user_info_storage.get_user_by_email(email):
            return UserInfoSchema.from_orm(user_info)
        raise ServiceItemSearchException(item_name='UserInfo',
                                         search_field='email',
                                         search_val=email)

    async def grant_role_to_user(self, user_id: UUID, role_id: UUID) -> None:
        try:
            role = await self._role_storage.generic.get(role_id)
            await self._user_info_storage.update_user_role(user_id, role)
        except ItemNotFoundException as exc:
            raise ServiceItemNotFound(item_name=exc.type_name,
                                      item_id=exc.item_id)

    async def save_user(self, email: str, password: str):
        if await self._user_info_storage.email_already_taken(email):
            raise ServiceUniqueFieldViolation(item_name='UserInfo',
                                              search_field='email',
                                              search_val=email)
        hashed_password = generate_hashed_password(password)
        role = await self._role_storage.get_default_role()
        user = UserInfo(email=email, password_hash=hashed_password,
                        user_role_id=role.id)
        await self._user_info_storage.add_user(user)

    async def update_credentials(self, user_id: UUID,
                                 changes: PatchUserInfoSchema) -> None:
        password_hash = generate_hashed_password(
            changes.password
        ) if changes.password else None
        if changes.email and await self._user_info_storage.email_already_taken(
            changes.email
        ):
            raise ServiceUniqueFieldViolation(item_name='UserInfo',
                                              search_field='email',
                                              search_val=changes.email)
        try:
            await self._user_info_storage.update_user_credentials(
                user_id, changes.email, password_hash
            )
        except ItemNotFoundException as exc:
            raise ServiceItemNotFound(item_name=exc.type_name,
                                      item_id=exc.item_id)
