from typing import Annotated
from uuid import UUID

from fastapi import Depends

from schemas.rating import UserRatingStats
from schemas.reviews import UserReviewsResponseSchema
from schemas.user_grade import UserSocialGradeResponse
from services.rating import MovieRatingService
from services.reviews import ReviewService

MovieRatingServiceDep = Annotated[MovieRatingService, Depends()]
ReviewServiceDep = Annotated[ReviewService, Depends()]


class UserGradeService:
    __RATING_GRADE_WEIGHT = 1.0
    __REVIEW_LIKE_GRADE_WEIGHT = 3.0
    __REVIEW_GRADE_WEIGHT = 10.0

    def __init__(self,
                 rating_service: MovieRatingServiceDep,
                 review_service: ReviewServiceDep):
        self.rating_service = rating_service
        self.review_service = review_service

    async def get_user_social_grade(self, user_id: UUID) -> UserSocialGradeResponse:
        rating_stat = await self.rating_service.get_user_ratings(user_id, 10, 0)
        review_stat = await self.review_service.get_user_reviews(user_id)
        return UserSocialGradeResponse(
            user_id=user_id,
            social_rating=UserGradeService._calc_rating(
                rating_stat, review_stat
            )
        )

    @classmethod
    def _calc_rating(cls, rating: UserRatingStats,
                     reviews: UserReviewsResponseSchema) -> float:
        return rating.total_count * cls.__RATING_GRADE_WEIGHT \
            + reviews.total_reviews_likes_count * cls.__REVIEW_LIKE_GRADE_WEIGHT \
            + reviews.total_count * cls.__REVIEW_GRADE_WEIGHT
