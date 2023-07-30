from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from starlette import status

from db.storage import StorageDep
from models.person import Person, PersonFilmWork
from models.base import IndexItemList
from services.base import BaseService, SearchQuery
from services.film import FilmService


class PersonService(BaseService):
    INDEX_NAME = 'persons'
    MOVIES_INDEX_NAME = 'movies'
    BASE_MODEL = Person

    def __init__(self, storage: StorageDep) -> None:
        super().__init__(storage)

    async def get_list(self,
                       page_number: int,
                       page_size: int,
                       query: str | None = None) -> IndexItemList:
        search_queries = [
            SearchQuery('full_name', query)
        ] if query else None
        return await self._get_items_list(
            page_number=page_number,
            page_size=page_size,
            search_queries=search_queries
        )

    async def get_person_films(self, person_id: UUID) -> list[PersonFilmWork]:
        if person := await self.get_by_id(person_id):
            person_film_ids = [film.id for film in person.films]
            results = []
            if not person_film_ids:
                return results
            person_films_data = await self._storage.get_many(FilmService.INDEX_NAME, person_film_ids)
            for film_data in person_films_data:
                results.append(
                    PersonFilmWork(
                        id=film_data['id'],
                        title=film_data['title'],
                        imdb_rating=film_data['imdb_rating']
                    )
                )
            return results
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Person not found')


PersonServiceDep = Annotated[PersonService, Depends()]
