from uuid import UUID
from fastapi import APIRouter
from core.auth import UserIdDep
from starlette import status
from schemas.bookmarks import BookmarkSchema
from services import BookmarkServiceDep


router = APIRouter()


@router.post('/bookmarks/add', description='Добавить фильм в закладки.')
async def create_movie_bookmark(data: BookmarkSchema, service: BookmarkServiceDep, user_id: UserIdDep):
    await service.add_bookmark(data.film_id, str(user_id))

@router.delete('/bookmarks/{bookmark_id}/delete', description='Удалить фильм из закладок')
async def delete_bookmark(bookmark_id: UUID, service: BookmarkServiceDep, _: UserIdDep):
    await service.remove_bookmark(bookmark_id)

# user_id только надо же?
@router.get('/bookmarks', description='Получить все закладки пользователя')
async def all_reviews(service: ReviewServiceDep, _: UserIdDep) -> list[Review]:
    return await service.get_reviews(query_params)

# просмотр списка закладок.
