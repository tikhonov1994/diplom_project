from sqlalchemy import select

from db.storage.generic_storage import GenericStorageMixin
from db.storage.session import DbSessionDep
from db.model import UserRole


class RoleStorage(GenericStorageMixin):
    def __init__(self, session: DbSessionDep):
        super().__init__(UserRole, session)
        self._session = session

    async def get_default_role(self) -> UserRole:
        stmt = select(UserRole).where(UserRole.name == 'user')
        if role := await self._session.execute(stmt):
            return role.first()
        role = UserRole(name='user')
        await self._session.add(role)
        return role
