from uuid import UUID

from db.storage import RatingStorageDep
from schemas.rating import MovieRatingStats


class MovieRatingServiceException(Exception):
    pass


class MovieRatingNotFound(MovieRatingServiceException):
    def __init__(self, movie_id: UUID) -> None:
        self._movie_id = movie_id

    def __str__(self) -> str:
        return f'Can\'t find Movie with id: \'{self._movie_id}\''


class MovieRatingService:
    def __init__(self, storage: RatingStorageDep):
        self._storage = storage

    async def set_rating(self, movie_id: UUID, user_id: UUID, value: int) -> None:
        await self._storage.upsert_user_rating_for_movie(user_id, movie_id, value)

    async def remove_rating(self, movie_id: UUID, user_id: UUID) -> None:
        if not await self._storage.remove_user_rating_for_movie(user_id, movie_id):
            raise MovieRatingNotFound(movie_id=movie_id)

    async def like(self, movie_id: UUID, user_id: UUID) -> None:
        await self.set_rating(movie_id, user_id, 10)

    async def dislike(self, movie_id: UUID, user_id: UUID) -> None:
        await self.set_rating(movie_id, user_id, 0)

    async def get_rating(self, movie_id: UUID) -> MovieRatingStats:
        records = await self._storage.get_rating_records_for_movie(movie_id)

        if len(records) == 0:
            raise MovieRatingNotFound(movie_id=movie_id)

        likes_count = dislikes_count = 0
        rating_value = 0.
        for rec in records:
            if rec.value == 10:
                likes_count += 1
            if rec.value == 0:
                dislikes_count += 1
            rating_value += rec.value
        rating_value /= len(records)

        return MovieRatingStats(
            movie_id=movie_id,
            likes_count=likes_count,
            dislikes_count=dislikes_count,
            rating_value=rating_value
        )
