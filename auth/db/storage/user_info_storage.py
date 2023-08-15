from uuid import UUID

from db.model import UserInfo, UserRole
from db.storage.generic_storage import (GenericStorageMixin,
                                        ItemNotFoundException)
from db.storage.session import DbSessionDep
from sqlalchemy import select


class UserInfoStorageException(Exception):
    pass


class UserEmailNotFoundException(UserInfoStorageException):
    def __init__(self, email: str) -> None:
        super().__init__()
        self._instance_email = email

    def __repr__(self) -> str:
        return f'User with email: \'{self._instance_email}\' not found'


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

    async def update_user_credentials(self, user_id: UUID, email: str | None, password_hash: str | None):
        if user := await self.generic.get(user_id):
            user: UserInfo
            if email:
                user.email = email
            if password_hash:
                user.password_hash = password_hash
            await self._session.flush((user,))
        else:
            raise ItemNotFoundException(UserInfo, user_id)

    async def add_user(self, user: UserInfo):
        await self.generic.add(user)

    async def get_user_by_email(self, email: str) -> UserInfo:
        stmt = select(UserInfo).where(UserInfo.email == email)
        if result := (await self._session.execute(stmt)).scalar():
            return result
        raise UserEmailNotFoundException(email=email)

    async def email_already_taken(self, email: str) -> bool:
        try:
            _ = await self.get_user_by_email(email)
        except UserEmailNotFoundException:
            return False
        return True
