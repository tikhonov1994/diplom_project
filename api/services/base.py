import logging
from collections import namedtuple
from uuid import UUID

from pydantic import BaseModel

from db.storage import AbstractStorage, NestedObjectFilter
from models.base import IndexItemList

SearchQuery = namedtuple('SearchQuery', 'field value')


class BaseService:
    INDEX_NAME: str
    BASE_MODEL = BaseModel

    def __init__(self, storage: AbstractStorage) -> None:
        self._storage = storage

    async def get_by_id(self, id_: UUID) -> BASE_MODEL | None:
        if doc := await self._storage.get(self.INDEX_NAME, id_):
            logging.debug('Got \'%s\'(id=\'%s\') from elastic', (self.BASE_MODEL.__name__, id_.hex))
            return self.BASE_MODEL.parse_obj(doc)
        logging.debug('\'%s\'(id=\'%s\') not found in elastic', (self.BASE_MODEL.__name__, id_.hex))
        return None

    async def _get_items_list(self,
                              page_number: int,
                              page_size: int,
                              search_queries: list[SearchQuery] | None = None,
                              sort: str | None = None,
                              nested_filter: NestedObjectFilter | None = None) -> IndexItemList:
        total_items, items_data = await self._storage.search(
            collection=self.INDEX_NAME,
            page_number=page_number,
            page_size=page_size,
            search_queries=search_queries,
            sort_by=sort,
            nested_object_filter=nested_filter
        )

        count = total_items
        total_pages = count // page_size + 1
        current_page = page_number

        return IndexItemList(
            count=count,
            total_pages=total_pages,
            prev=current_page - 1 if 1 < current_page <= (total_pages + 1) else None,
            next=(current_page + 1) if current_page < total_pages else None,
            results=[self.BASE_MODEL.parse_obj(item_obj)
                     for item_obj in items_data],
        )
