from uuid import UUID

from services.base import MongoServiceBase
from schemas.rating import MovieRatingStats


class MovieRatingService(MongoServiceBase):
    async def set_rating(self, movie_id: UUID, user_id: UUID, value: int) -> None:
        ...

    async def remove_rating(self, movie_id: UUID, user_id: UUID) -> None:
        ...

    async def like(self, movie_id: UUID, user_id: UUID) -> None:
        await self.set_rating(movie_id, user_id, 10)

    async def dislike(self, movie_id: UUID, user_id: UUID) -> None:
        await self.set_rating(movie_id, user_id, 0)

    async def get_rating(self, movie_id: UUID) -> MovieRatingStats:
        ...
