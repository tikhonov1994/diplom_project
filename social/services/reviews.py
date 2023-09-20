from db.storage import ReviewStorageDep
from uuid import UUID


class ReviewService:
    def __init__(self, mongo_storage: ReviewStorageDep) -> None:
        self.mongo_storage = mongo_storage

    async def add_review(self, text: str, user_id: UUID, film_id: UUID, author_rating: int):
        await self.mongo_storage.insert_review(text, user_id, author_rating, film_id)
