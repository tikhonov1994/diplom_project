from uuid import UUID

from db.storage import UserRoleStorageDep, ItemNotFoundException, DbConflictException
from db.model import UserRole
from schemas.user import UserRoleSchema
from services.exceptions import (ServiceItemNotFound,
                                 ServiceConflictOnAddError,
                                 ServiceConflictOnDeleteError)


class RoleService:
    def __init__(self, storage: UserRoleStorageDep):
        self._storage = storage

    async def get_roles(self) -> list[UserRoleSchema]:
        return [UserRoleSchema.from_orm(role) for role in await self._storage.generic.list()]

    async def add_role(self, role_name: str) -> None:
        try:
            await self._storage.generic.add(UserRole(name=role_name))
        except DbConflictException:
            raise ServiceConflictOnAddError(item_dict={'name': role_name})

    async def delete_role(self, role_id: UUID) -> None:
        try:
            await self._storage.generic.delete(role_id)
        except ItemNotFoundException as exc:
            raise ServiceItemNotFound(item_name=exc.type_name, item_id=exc.item_id)
        except DbConflictException:
            raise ServiceConflictOnDeleteError(item_name='Role', item_id=role_id)
