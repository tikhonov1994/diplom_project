from uuid import UUID
from motor import motor_asyncio
from core.config import app_config


class MongoStorage:
    def __init__(self) -> None:
        self.client = motor_asyncio.AsyncIOMotorClient(app_config.mongo.host, app_config.mongo.port)
        self.db = self.client.someDb
        self.reviews = self.db.reviews
        self.loop = self.client.get_io_loop()

    async def prepare_review(self, text: str, user_id: UUID, author_rating: int, film_id: UUID):
        document = {'user': user_id, 'text': text, 'author_rating': author_rating, 'film': film_id}
        await self.reviews.insert_one(document)

    async def insert_review(self, text: str, user_id: UUID, author_rating: int, film_id: UUID):
        self.loop.run_until_complete(self.prepare_review(text, user_id, author_rating, film_id))
