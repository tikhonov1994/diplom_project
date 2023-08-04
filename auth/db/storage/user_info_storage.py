from uuid import UUID

from db.storage.generic_storage import GenericStorageMixin, ItemNotFoundException
from db.storage.session import DbSessionDep
from db.model import UserInfo, UserRole


class UserInfoStorage(GenericStorageMixin):
    def __init__(self, session: DbSessionDep):
        super().__init__(UserInfo, session)
        self._session = session

    async def update_user_role(self, user_id: UUID, role: UserRole):
        if user := await self.generic.get(user_id):
            user.role = role
            await self._session.flush((user,))
        else:
            raise ItemNotFoundException(UserInfo, user_id)
    
    async def add_user(self, user: UserInfo):
        await self._session.add(user)
