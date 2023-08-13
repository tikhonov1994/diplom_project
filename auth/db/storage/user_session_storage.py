from datetime import datetime
from db.storage.generic_storage import GenericStorageMixin, ItemNotFoundException
from db.storage.session import DbSessionDep
from db.model import UserSession
from uuid import UUID


class UserSessionStorage(GenericStorageMixin):
    def __init__(self, session: DbSessionDep):
        super().__init__(UserSession, session)
        self._session = session

    async def add_session(self, user_session: UserSession) -> None:
        await self.generic.add(user_session)

    async def update_refresh_token(self, user_session_id: UUID, refresh_token: str,
                                   refresh_token_jti: str):
        if user_session := await self.generic.get(user_session_id):
            user_session.refresh_token = refresh_token
            user_session.refresh_token_jti = refresh_token_jti
            await self._session.flush((user_session,))
        else:
            raise ItemNotFoundException(UserSession, user_session)

    async def close_session(self, user_session: UserSession):
        user_session.end_at = datetime.now()
        await self._session.flush((user_session,))