from typing import Annotated
from uuid import UUID

from fastapi import Depends

from db.storage import StorageDep
from models.film import Film
from models.base import IndexItemList
from services.base import BaseService, SearchQuery, NestedObjectFilter


class FilmService(BaseService):
    INDEX_NAME = 'movies'
    BASE_MODEL = Film

    def __init__(self, storage: StorageDep) -> None:
        super().__init__(storage)

    async def get_list(self,
                       page_number: int,
                       page_size: int,
                       query: str | None = None,
                       sort: str | None = None,
                       genre_id: UUID | None = None) -> IndexItemList:
        search_queries = [
            SearchQuery('title', query),
            SearchQuery('description', query)
        ] if query else None
        nested_filter = NestedObjectFilter('genre', 'id', str(genre_id)) if genre_id else None
        return await self._get_items_list(
            page_number=page_number,
            page_size=page_size,
            search_queries=search_queries,
            sort=sort,
            nested_filter=nested_filter
        )


FilmServiceDep = Annotated[FilmService, Depends()]
