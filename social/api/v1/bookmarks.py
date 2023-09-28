from uuid import UUID
from fastapi import APIRouter
from core.auth import UserIdDep
from models.bookmark import Bookmark
from schemas.bookmarks import BookmarkSchema
from services import BookmarkServiceDep

router = APIRouter()


@router.post('/bookmarks/add', description='Добавить фильм в закладки.')
async def create_movie_bookmark(data: BookmarkSchema, service: BookmarkServiceDep, user_id: UserIdDep):
    await service.add_bookmark(data.film_id, str(user_id))


@router.delete('/bookmarks/{bookmark_id}/delete', description='Удалить фильм из закладок')
async def delete_bookmark(bookmark_id: UUID, service: BookmarkServiceDep, _: UserIdDep):
    await service.remove_bookmark(bookmark_id)


@router.get('/bookmarks', description='Получить все закладки пользователя')
async def get_all_user_bookmarks(service: BookmarkServiceDep, user_id: UserIdDep) -> list[Bookmark]:
    return await service.get_user_bookmarks_list(user_id)
