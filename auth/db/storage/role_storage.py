from sqlalchemy import select

from core.config import app_config
from db.model import UserRole
from db.storage.generic_storage import GenericStorageMixin
from db.storage.session import DbSessionDep
from utils.tracer import sub_span


class RoleStorage(GenericStorageMixin):
    def __init__(self, session: DbSessionDep):
        super().__init__(UserRole, session)
        self._session = session

    @sub_span
    async def get_default_role(self) -> UserRole:
        stmt = select(UserRole).where(UserRole.name == app_config.api.default_user_role)
        if role := (await self._session.execute(stmt)).first():
            return role[0]
        role = UserRole(name=app_config.api.default_user_role)
        await self.generic.add(role)
        return role
