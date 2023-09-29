from typing import List
from uuid import UUID

from db.storage import BookmarkStorageDep
from models.bookmark import Bookmark


class BookmarkNotFound(Exception):
    def __init__(self, bookmark_id: UUID) -> None:
        self._bookmark_id = bookmark_id

    def __str__(self) -> str:
        return f'Can\'t find bookmark with id: \'{self._bookmark_id}\''


class BookmarksService:
    def __init__(self, storage: BookmarkStorageDep):
        self._storage = storage

    async def add_bookmark(self, film_id: UUID, user_id: UUID) -> None:
        await self._storage.insert_bookmark(film_id, user_id)

    async def remove_bookmark(self, bookmark_id: UUID) -> None:
        if not await self._storage.remove_bookmark(bookmark_id):
            raise BookmarkNotFound(bookmark_id=bookmark_id)

    async def get_user_bookmarks_list(self, user_id: UUID) -> List[Bookmark]:
        return await self._storage.get_bookmarks(user_id)

