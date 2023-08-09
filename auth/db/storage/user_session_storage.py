from db.storage.generic_storage import GenericStorageMixin, ItemNotFoundException
from db.storage.session import DbSessionDep
from db.model import UserSession


class UserSessionStorage(GenericStorageMixin):
    def __init__(self, session: DbSessionDep):
        super().__init__(UserSession, session)
        self._session = session

    async def add_session(self, user_session: UserSession) -> None:
        await self.generic.add(user_session)
