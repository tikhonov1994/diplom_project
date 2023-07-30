from typing import Annotated

from fastapi import Depends

from db.storage import StorageDep
from models.genre import Genre
from services.base import BaseService


class GenreService(BaseService):
    INDEX_NAME = 'genres'
    BASE_MODEL = Genre

    def __init__(self, storage: StorageDep) -> None:
        super().__init__(storage)

    async def get_all(self) -> list[Genre]:
        return (await self._get_items_list(page_number=1, page_size=10000)).results


GenreServiceDep = Annotated[GenreService, Depends()]
