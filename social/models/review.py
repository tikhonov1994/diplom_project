from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Review(BaseModel):
    review_id: UUID | None
    film_id: UUID | None
    text: str
    added: datetime | None
    user_id: UUID | None
    author_rating: int


class ReviewRating(BaseModel):
    review_id: UUID
    likes_count: int
    dislikes_count: int


class ReviewAssessment(BaseModel):
    review_id: UUID
    user_id: UUID
    liked: bool
