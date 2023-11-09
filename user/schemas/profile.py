from enum import Enum

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserProfileSchema(BaseModel):
    name: str
    surname: str
    country: str
    time_zone: str
    phone_number: PhoneNumber


class AvatarStatusesSchema(str, Enum):
    WITHOUT = 'WITHOUT'
    ON_INSPECTION = 'ON_INSPECTION'
    ACCEPTED = 'ACCEPTED'
    NON_ACCEPTED = 'NON_ACCEPTED'


class UserRatingStatsSchema(BaseModel):
    ratings: list
    total_count: int
    average_rating: int


class UserReviewsStatsSchema(BaseModel):
    reviews: list
    total_count: int
    total_count_positive_reviews: int
    total_count_negative_reviews: int
    total_reviews_likes_count: int
    total_reviews_dislikes_count: int


class UserProfileResponseSchema(BaseModel):
    name: str
    surname: str
    country: str
    time_zone: str
    phone_number: str
    avatar_link: str | None
    avatar_status: str | None

    rating_stats: UserRatingStatsSchema
    review_stats: UserReviewsStatsSchema


