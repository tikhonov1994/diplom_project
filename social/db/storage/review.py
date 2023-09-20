from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorCollection

from db.storage.base import MongoStorageBase


class ReviewStorage(MongoStorageBase):
    @property
    def reviews(self) -> AsyncIOMotorCollection:
        return self.db.reviews

    async def prepare_review(self, text: str, user_id: UUID, author_rating: int, film_id: UUID):
        document = {'user': user_id, 'text': text, 'author_rating': author_rating, 'film': film_id}
        await self.reviews.insert_one(document)

    async def insert_review(self, text: str, user_id: UUID, author_rating: int, film_id: UUID):
        await self.prepare_review(text, user_id, author_rating, film_id)
