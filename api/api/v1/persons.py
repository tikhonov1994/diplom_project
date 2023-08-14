from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache
from starlette import status

from core.config import app_config as config
from core.auth import UserRequiredDep
from models.person import Person, PersonFilmWork, PersonList
from services.person import PersonServiceDep

router = APIRouter()


@router.get(path='/{person_id:uuid}',
            description='Получение информации о кинодеятеле по его id.',
            response_model=Person)
@cache(expire=config.api.cache_expire_seconds)
async def person_details(person_id: UUID,
                         _: UserRequiredDep,
                         service: PersonServiceDep) -> Person:
    if person := await service.get_by_id(person_id):
        return person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Person not found')


@router.get(path='/search',
            description='Поиск кинодеятелей.',
            response_model=PersonList)
@cache(expire=config.api.cache_expire_seconds)
async def search_persons(
        service: PersonServiceDep,
        page_number: Annotated[int, Query(gt=0, lt=10000)] = 1,
        page_size: Annotated[int, Query(gt=0, lt=10000)] = 50,
        query: str = "") -> PersonList:
    return await service.get_list(page_number, page_size, query)


@router.get(path='/{person_id}/film',
            description='Получение списка кинопроизведений, к которым имеет отношение кинодеятель.',
            response_model=list[PersonFilmWork])
@cache(expire=config.api.cache_expire_seconds)
async def person_films(person_id: UUID, service: PersonServiceDep) -> list[PersonFilmWork]:
    return await service.get_person_films(person_id)
