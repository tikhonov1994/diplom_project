from db.storage import UserRoleStorageDep
from api.models import UserRoleSchema


class RoleService:
    def __init__(self, storage: UserRoleStorageDep):
        self._storage = storage

    async def get_roles(self) -> list[UserRoleSchema]:
        return await self._storage.list()
