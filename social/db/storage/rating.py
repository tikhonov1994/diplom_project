from datetime import datetime
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorCollection

from db.storage.base import MongoStorageBase
from models.rating import EntityRating


class RatingStorage(MongoStorageBase):
    @property
    def movie_likes(self) -> AsyncIOMotorCollection:
        return self.db.movieLikes

    async def get_rating_records_for_movie(self, movie_id: UUID) -> list[EntityRating]:
        cursor = self.movie_likes.find({'entity_id': {'$eq': movie_id}})
        return [EntityRating.parse_obj(doc) for doc in await cursor.to_list(length=None)]

    async def upsert_user_rating_for_movie(self, user_id: UUID, movie_id: UUID, rating_value: int) -> None:
        new_doc = EntityRating(
            user_id=user_id,
            entity_id=movie_id,
            value=rating_value,
            added=datetime.now()
        )

        await self.movie_likes.replace_one({'$and': [
            {'user_id': {'$eq': user_id}},
            {'entity_id': {'$eq': movie_id}}
        ]}, new_doc.dict(), upsert=True)

    async def remove_user_rating_for_movie(self, user_id: UUID, movie_id: UUID) -> None:
        await self.movie_likes.delete_one({'$and': [
            {'user_id': {'$eq': user_id}},
            {'entity_id': {'$eq': movie_id}}
        ]})
