from typing import Annotated, Optional, Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache
from starlette import status

from core.config import app_config as config
from core.auth import UserRequiredDep
from models.film import Film, FilmList
from services.film import FilmServiceDep

router = APIRouter()


@router.get('/{film_id}', response_model=Film, description='Получить фильм по id')
@cache(expire=config.api.cache_expire_seconds)
async def film_details(film_id: UUID, service: FilmServiceDep, _: UserRequiredDep) -> Film:
    if film := await service.get_by_id(film_id):
        return film
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Film not found')


@router.get('/',
            description='Получение списка фильмов с фильтрацией и сортировкой.',
            response_model=FilmList)
@cache(expire=config.api.cache_expire_seconds)
async def films_filter(service: FilmServiceDep, sort: Optional[Literal["imdb_rating"]] = None, genre: UUID | None = None,
                       page_number: Annotated[int, Query(gt=0)] = 1,
                       page_size: Annotated[int, Query(gt=0, lt=10_000)] = 50) -> FilmList:
    return await service.get_list(
        page_number=page_number,
        page_size=page_size,
        sort=sort,
        genre_id=genre
    )


@router.get('/search/',
            description='Получение списка фильмов с поиском.',
            response_model=FilmList)
@cache(expire=config.api.cache_expire_seconds)
async def films_search(service: FilmServiceDep, query: str | None = None,
                       page_number: Annotated[int, Query(gt=0)] = 1,
                       page_size: Annotated[int, Query(gt=0, lt=10_000)] = 50) -> FilmList:
    return await service.get_list(
        page_number=page_number,
        page_size=page_size,
        query=query
    )
