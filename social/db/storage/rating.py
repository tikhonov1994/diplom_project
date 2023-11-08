from datetime import datetime
from typing import List
from uuid import UUID

from db.storage.base import MongoStorageBase
from models.rating import EntityRating
from motor.core import AgnosticCollection


class RatingStorage(MongoStorageBase):
    @property
    def movie_likes(self) -> AgnosticCollection:
        return self.db.movieLikes

    async def get_rating_records_for_movie(self, movie_id: UUID) -> List[EntityRating]:
        cursor = self.movie_likes.find({'entity_id': {'$eq': movie_id}})
        return [EntityRating.parse_obj(doc) for doc in await cursor.to_list(length=None)]  # type: ignore[arg-type]

    async def get_rating_records_for_user(self, user_id: UUID, limit, offset) -> List[EntityRating]:
        cursor = self.movie_likes.find({'user_id': {'$eq': user_id}})
        cursor.sort('added', -1).skip(offset).limit(limit)
        return [EntityRating.parse_obj(doc) for doc in await cursor.to_list(length=None)]  # type: ignore[arg-type]

    async def get_user_ratings_total_count(self, user_id: UUID) -> int:
        cursor = self.movie_likes.count_documents({'user_id': {'$eq': user_id}})

        return await cursor

    async def get_user_ratings_total_sum(self, user_id: UUID) -> list[int]:
        cursor = self.movie_likes.aggregate([
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': "null",
                'total_sum': {
                    '$sum': "$value"
                }}}])

        return await cursor.to_list(length=None)

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

    async def remove_user_rating_for_movie(self, user_id: UUID, movie_id: UUID) -> bool:
        deletion_result = await self.movie_likes.delete_one({'$and': [
            {'user_id': {'$eq': user_id}},
            {'entity_id': {'$eq': movie_id}}
        ]})
        return deletion_result.deleted_count != 0
