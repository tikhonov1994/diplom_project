from abc import ABC, abstractmethod
from collections import namedtuple
from uuid import UUID

CollectionResultType = dict[str, any]
NestedObjectFilter = namedtuple('NestedObjectFilter',
                                'name field value')


class AbstractStorage(ABC):
    @abstractmethod
    async def get(self, collection: str, item_id: UUID) -> CollectionResultType | None:
        raise NotImplementedError

    @abstractmethod
    async def search(
            self,
            collection: str,
            page_number: int,
            page_size: int,
            search_queries: tuple[str, str] | None = None,
            sort_by: str | None = None,
            nested_object_filter: NestedObjectFilter | None = None
    ) -> tuple[int, list[CollectionResultType]]:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, collection: str, id_list: list[UUID]) -> list[CollectionResultType]:
        raise NotImplementedError
