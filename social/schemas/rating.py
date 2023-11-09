from uuid import UUID

from pydantic import BaseModel
from models.rating import EntityRating


class MovieRatingStats(BaseModel):
    movie_id: UUID
    likes_count: int
    dislikes_count: int
    rating_value: float


class UserRatingStats(BaseModel):
    ratings: list[EntityRating]
    total_count: int
    average_rating: int


class AssessMovieSchema(BaseModel):
    movie_id: UUID


class RateMovieSchema(AssessMovieSchema):
    rating_value: int
