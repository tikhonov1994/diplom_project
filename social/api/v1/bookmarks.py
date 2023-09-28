from uuid import UUID
from fastapi import APIRouter, HTTPException
from core.auth import UserIdDep
from models.bookmark import Bookmark
from schemas.bookmarks import BookmarkSchema
from services import BookmarkServiceDep
from services.bookmarks import BookmarkNotFound
from starlette import status


router = APIRouter()


@router.post('/add', description='Добавить фильм в закладки.')
async def create_movie_bookmark(data: BookmarkSchema, service: BookmarkServiceDep, user_id: UserIdDep):
    await service.add_bookmark(data.film_id, str(user_id))


@router.delete('/{bookmark_id}/delete', description='Удалить фильм из закладок')
async def delete_bookmark(bookmark_id: UUID, service: BookmarkServiceDep, _: UserIdDep):
    try:
        await service.remove_bookmark(bookmark_id)
    except BookmarkNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.get('', description='Получить все закладки пользователя')
async def get_user_bookmarks(service: BookmarkServiceDep, user_id: UserIdDep) -> list[Bookmark]:
    return await service.get_user_bookmarks_list(user_id)
