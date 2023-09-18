from uuid import UUID

from pydantic import BaseModel


class MovieRatingStats(BaseModel):
    movie_id: UUID
    likes_count: int
    dislikes_count: int
    rating_value: float


class AssessMovieSchema(BaseModel):
    movie_id: UUID
    user_id: UUID


class RateMovieSchema(AssessMovieSchema):
    rating_value: int
