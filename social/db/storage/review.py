from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from db.storage.base import MongoStorageBase
from models.review import Review, ReviewAssessment, ReviewRating
from motor.core import AgnosticCollection


class ReviewStorage(MongoStorageBase):
    @property
    def reviews(self) -> AgnosticCollection:
        return self.db.reviews

    @property
    def review_assessments(self) -> AgnosticCollection:
        return self.db.review_assessments

    async def insert_review(self, text: str, user_id: UUID, author_rating: int, film_id: UUID):
        document = Review(
            review_id=uuid4(),
            user_id=user_id,
            film_id=film_id,
            text=text,
            author_rating=author_rating,
            added=datetime.now()
        )
        await self.reviews.insert_one(document.dict())

    async def get_reviews(self, sort=None, filter_query=None) -> List[Review]:
        if filter_query:
            cursor = self.reviews.find(filter_query)
        else:
            cursor = self.reviews.find()
        if sort:
            cursor = cursor.sort(*sort)
        return [Review.parse_obj(doc) for doc in await cursor.to_list(length=None)]  # type: ignore[arg-type]

    async def update_review(self, text: str, user_id: UUID, author_rating: int, film_id: UUID,
                            review_id: UUID):
        document = Review(
            review_id=review_id,
            user_id=user_id,
            film_id=film_id,
            text=text,
            author_rating=author_rating,
            added=datetime.now()
        )

        await self.reviews.replace_one({'review_id': {'$eq': review_id}},
                                       document.dict(), upsert=True)

    async def delete_review(self, review_id: UUID):
        await self.reviews.delete_one({'review_id': {'$eq': review_id}})

    async def upset_assessment(self, liked: bool, user_id: UUID, review_id: UUID):
        doc = ReviewAssessment(
            review_id=review_id,
            liked=liked,
            user_id=user_id
        )
        await self.review_assessments.replace_one({'$and': [
            {'user_id': {'$eq': user_id}},
            {'review_id': {'$eq': review_id}}
        ]}, doc.dict(), upsert=True)

    async def get_review_rating(self, review_id: UUID) -> ReviewRating:
        cursor_likes = self.review_assessments.find(
            {'$and': [
                {'review_id': {'$eq': review_id}},
                {'liked': {'$eq': True}}
            ]})
        likes_count = len(await cursor_likes.to_list(length=None))  # type: ignore[arg-type]
        cursor_dislikes = self.review_assessments.find(
            {'$and': [
                {'review_id': {'$eq': review_id}},
                {'liked': {'$eq': False}}
            ]})
        dislikes_count = len(await cursor_dislikes.to_list(length=None))  # type: ignore[arg-type]
        return ReviewRating(review_id=review_id, likes_count=likes_count, dislikes_count=dislikes_count)

    async def delete_assessment(self, user_id: UUID, review_id: UUID):
        await self.review_assessments.delete_one({'$and': [
            {'user_id': {'$eq': user_id}},
            {'review_id': {'$eq': review_id}}
        ]})
