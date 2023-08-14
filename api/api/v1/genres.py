from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from pydantic import BaseModel, Field
from starlette import status

from core.config import app_config as config
from core.auth import UserRequiredDep
from services.genre import GenreServiceDep

router = APIRouter()


class Genre(BaseModel):
    uuid: UUID = Field(alias='id')
    name: str


@router.get(path='/{genre_id}',
            description='Получение жанра по его id.',
            response_model=Genre)
@cache(expire=config.api.cache_expire_seconds)
async def genre_details(genre_id: UUID,
                        _: UserRequiredDep,
                        service: GenreServiceDep) -> Genre:
    if genre := await service.get_by_id(genre_id):
        return genre
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Genre not found')


@router.get(path='/',
            description='Получение полного списка жанров.',
            response_model=list[Genre])
@cache(expire=config.api.cache_expire_seconds)
async def genre_list(service: GenreServiceDep) -> list[Genre]:
    return await service.get_all()
