from typing import Generic, TypeVar, Type
from uuid import UUID

from sqlalchemy import select

from db.storage.session import DbSessionDep
from db.model import Base

DbModelType = TypeVar('DbModelType')


class GenericStorageException(Exception):
    pass


class ItemNotFoundException(GenericStorageException):
    def __init__(self, item_type: Type[Base], item_id: UUID) -> None:
        super().__init__()
        self._instance_t = item_type
        self._instance_id = item_id

    def __repr__(self) -> str:
        return f'Item of type \'{self._instance_t}\' with id: \'{self._instance_id}\' not found'


class GenericStorage(Generic[DbModelType]):
    def __init__(self, session: DbSessionDep):
        self._session = session

    async def get(self, item_id: UUID) -> DbModelType:
        if result := await self._session.get(DbModelType, item_id):
            return result
        raise ItemNotFoundException(item_type=DbModelType, item_id=item_id)

    async def list(self) -> list[DbModelType]:
        return await self._session.scalars(select(DbModelType)).all()

    async def add(self, item: DbModelType) -> None:
        await self._session.add(item)

    async def delete(self, item_id: UUID) -> None:
        _instance = await self.get(item_id)
        await self._session.delete(_instance)
        # await self._session.flush()
