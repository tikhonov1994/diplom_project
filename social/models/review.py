from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Review(BaseModel):
    review_id: UUID
    film_id: UUID
    text: str
    added: datetime
    user_id: UUID
    author_rating: int


class ReviewRating(BaseModel):
    review_id: UUID
    likes_count: int
    dislikes_count: int


class ReviewAssessment(BaseModel):
    review_id: UUID
    user_id: UUID
    liked: bool
    added: datetime
