from uuid import UUID

from pydantic import BaseModel


class ReviewSchema(BaseModel):
    film_id: UUID
    text: str
    author_rating: int


class DailyTopReviewsSchema(BaseModel):
    review_id: UUID
    film_id: UUID
    text: str
    likes_count: int

