from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from db.storage.base import MongoStorageBase
from models.bookmark import Bookmark
from motor.core import AgnosticCollection


class BookmarkStorage(MongoStorageBase):
    @property
    def bookmarks(self) -> AgnosticCollection:
        return self.db.bookmarks

    async def insert_bookmark(self, film_id: UUID, user_id: UUID):
        document = Bookmark(
            bookmark_id=uuid4(),
            user_id=user_id,
            film_id=film_id,
            added=datetime.now()
        )
        await self.bookmarks.insert_one(document.dict())

    async def remove_bookmark(self, bookmark_id: UUID) -> bool:
        deletion_result = await self.bookmarks.delete_one({'bookmark_id': {'$eq': bookmark_id}})
        return deletion_result.deleted_count != 0

    async def get_bookmarks(self, user_id: UUID) -> List[Bookmark]:
        cursor = self.bookmarks.find({'user_id': {'$eq': user_id}})

        return [Bookmark.parse_obj(doc) for doc in await cursor.to_list(length=None)]  # type: ignore[arg-type]
