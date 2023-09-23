from db.storage import ReviewStorageDep
from uuid import UUID

from models.review import ReviewRating


class ReviewService:
    def __init__(self, mongo_storage: ReviewStorageDep) -> None:
        self.mongo_storage = mongo_storage

    async def add_review(self, text: str, user_id: UUID, film_id: UUID, author_rating: int):
        await self.mongo_storage.insert_review(text, user_id, author_rating, film_id)

    async def update_review(self, text: str, user_id: UUID, author_rating: int, film_id: UUID,
                            review_id: UUID) -> None:
        await self.mongo_storage.update_review(text, user_id, author_rating, film_id, review_id)
    
    async def get_all_reviews(self):
        return await self.mongo_storage.get_all_reviews()
    
    async def delete_review(self, review_id: UUID):
        await self.mongo_storage.delete_review(review_id)

    async def add_assessment_to_review(self, review_id: UUID, user_id: UUID, liked: bool):
        await self.mongo_storage.upset_assessment(liked, user_id, review_id)

    async def delete_assessment_review(self, review_id: UUID, user_id: UUID):
        await self.mongo_storage.delete_assessment(user_id, review_id)

    async def get_review_rating(self, review_id: UUID) -> ReviewRating:
        return await self.mongo_storage.get_review_rating(review_id)
