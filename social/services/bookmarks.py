from uuid import UUID

from db.storage import BookmarkStorageDep
from models.bookmark import Bookmark


class BookmarksService:
    def __init__(self, storage: BookmarkStorageDep):
        self._storage = storage

    async def add_bookmark(self, film_id: UUID, user_id: UUID) -> None:
        await self._storage.insert_bookmark(film_id, user_id)

    async def remove_bookmark(self, bookmark_id: UUID) -> None:
        await self._storage.remove_bookmark(bookmark_id)

    async def get_user_bookmarks_list(self, user_id: UUID) -> list[Bookmark]:
        return await self._storage.get_bookmarks(user_id)

