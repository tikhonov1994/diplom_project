from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from models.review import ReviewRating


class ReviewSchema(BaseModel):
    film_id: UUID
    text: str
    author_rating: int


class DailyTopReviewsSchema(BaseModel):
    review_id: UUID
    film_id: UUID
    text: str
    likes_count: int


class UserReviewInfoSchema(ReviewSchema):
    review_id: UUID
    added: datetime
    rating: ReviewRating


class UserReviewsResponseSchema(BaseModel):
    reviews: list[UserReviewInfoSchema]
    total_count: int
    total_count_positive_reviews: int
    total_count_negative_reviews: int
    total_reviews_likes_count: int
    total_reviews_dislikes_count: int


