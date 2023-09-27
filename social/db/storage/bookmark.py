from datetime import datetime
from uuid import UUID, uuid4

from db.storage.base import MongoStorageBase
from models.bookmark import Bookmark
from motor.motor_asyncio import AsyncIOMotorCollection


class BookmarkStorage(MongoStorageBase):
    @property
    def bookmarks(self) -> AsyncIOMotorCollection:
        return self.db.bookmarks

    async def insert_bookmark(self, film_id: UUID, user_id: UUID):
        document = Bookmark(
            bookmark_id=uuid4(),
            user_id=user_id,
            film_id=film_id,
            added=datetime.now()
        )
        await self.bookmarks.insert_one(document.dict())

    async def remove_bookmark(self, bookmark_id: UUID):
        await self.bookmarks.delete_one({'bookmark_id': {'$eq': bookmark_id}})
    
    async def get_reviews(self, sort: set | None = None, filter_query: dict | None = None) -> list[Review]:
        if filter_query:
            cursor = self.reviews.find(filter_query)
        else:
            cursor = self.reviews.find()
        if sort:
            cursor = cursor.sort(*sort)
        return [Review.parse_obj(doc) for doc in await cursor.to_list(length=None)]


    async def get_review_rating(self, review_id: UUID) -> ReviewRating:
        cursor_likes = self.review_assessments.find(
            {'$and': [
            {'review_id': {'$eq': review_id}},
            {'liked': {'$eq': True}}
        ]})
        likes_count = len(await cursor_likes.to_list(length=None))
        cursor_dislikes = self.review_assessments.find(
            {'$and': [
            {'review_id': {'$eq': review_id}},
            {'liked': {'$eq': False}}
        ]})
        dislikes_count = len(await cursor_dislikes.to_list(length=None))
        return ReviewRating(review_id=review_id, likes_count=likes_count, dislikes_count=dislikes_count)

    async def delete_assessment(self, user_id: UUID, review_id: UUID):
        await self.review_assessments.delete_one({'$and': [
            {'user_id': {'$eq': user_id}},
            {'review_id': {'$eq': review_id}}
        ]})