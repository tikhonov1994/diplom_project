from uuid import UUID

from db.storage import UserInfoStorageDep, UserRoleStorageDep, ItemNotFoundException
from services.exceptions import ServiceItemNotFound
from schemas.user import UserInfoSchema


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
