from typing import Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.model import Base
from utils.tracer import sub_span

DbModelType = TypeVar('DbModelType')


class GenericStorageException(Exception):
    pass


class ItemNotFoundException(GenericStorageException):
    def __init__(self, item_type: Type[Base], item_id: UUID) -> None:
        super().__init__()
        self.item_type = item_type
        self.item_id = item_id

    @property
    def type_name(self) -> str:
        return self.item_type.__name__

    def __str__(self) -> str:
        return f'Item of type \'{self.type_name}\' with id: \'{self.item_id}\' not found'


class DbConflictException(GenericStorageException):
    pass


class GenericStorage(Generic[DbModelType]):
    def __init__(self, item_type: Type[Base], session: AsyncSession):
        self._type = item_type
        self._session = session

    @sub_span
    async def get(self, item_id: UUID) -> DbModelType:
        if result := await self._session.get(self._type, item_id):
            return result
        raise ItemNotFoundException(item_type=self._type, item_id=item_id)

    @sub_span
    async def list(self) -> list[DbModelType]:
        scalars = await self._session.scalars(select(self._type))
        return list(scalars.all())

    @sub_span
    async def add(self, item: DbModelType) -> None:
        try:
            self._session.add(item)
            await self._session.flush()
            await self._session.refresh(item)
        except IntegrityError:
            raise DbConflictException

    @sub_span
    async def delete(self, item_id: UUID) -> None:
        _instance = await self.get(item_id)
        try:
            await self._session.delete(_instance)
            await self._session.flush()
        except IntegrityError:
            raise DbConflictException


def get_generic_storage(item_type: Type[Base], session: AsyncSession) -> GenericStorage:
    return GenericStorage[item_type](item_type, session)


class GenericStorageMixin(Generic[DbModelType]):
    def __init__(self, item_type: Type[Base], session: AsyncSession) -> None:
        self._type = item_type
        self._generic = get_generic_storage(item_type, session)

    @property
    def generic(self) -> GenericStorage[DbModelType]:
        return self._generic


__all__ = ['ItemNotFoundException', 'DbConflictException', 'GenericStorageMixin']
