from datetime import datetime
from uuid import UUID

from db.model import UserSession
from db.storage.generic_storage import (GenericStorageMixin,
                                        ItemNotFoundException)
from db.storage.session import DbSessionDep
from sqlalchemy import select


class UserSessionStorage(GenericStorageMixin):
    def __init__(self, session: DbSessionDep):
        super().__init__(UserSession, session)
        self._session = session

    async def add_session(self, user_session: UserSession) -> None:
        await self.generic.add(user_session)

    async def get_session_by_refresh_token(self, refresh_token: UUID) -> UserSession:
        stmt = select(UserSession).where(UserSession.refresh_token_jti == refresh_token)
        if session := (await self._session.execute(stmt)).first():
            return session[0]

    async def refresh_session(self, user_session_id: UUID, refresh_token_jti: UUID, end_at):
        if user_session := await self.generic.get(user_session_id):
            user_session.refresh_token_jti = refresh_token_jti
            user_session.end_at = end_at
            await self._session.flush((user_session,))
        else:
            raise ItemNotFoundException(UserSession, user_session)

    async def close_session(self, user_session: UserSession):
        user_session.end_at = datetime.now()
        await self._session.flush((user_session,))
