from typing import Annotated, List  # type: ignore[attr-defined]
from uuid import UUID

from core.auth import UserIdDep
from fastapi import APIRouter, Depends
from models.review import Review, ReviewRating
from schemas.reviews import ReviewSchema
from schemas.reviews_query import QueryParams

from services import ReviewServiceDep

router = APIRouter()


@router.post('/add', description='Отправить рецензию')
async def send_review(validated_data: ReviewSchema,
                      service: ReviewServiceDep,
                      user_id: UserIdDep) -> dict:
    await service.add_review(validated_data.text, user_id, validated_data.film_id, validated_data.author_rating)
    return {'ok': True}


@router.post('/{review_id}/edit', description='Изменить рецензию')
async def update_review(review_id: UUID, validated_data: ReviewSchema,
                        service: ReviewServiceDep,
                        user_id: UserIdDep):
    await service.update_review(validated_data.text, user_id, validated_data.author_rating,
                                validated_data.film_id, review_id)


@router.get('', description='Все рецензии')
async def all_reviews(query_params: Annotated[QueryParams, Depends()],
                      service: ReviewServiceDep, _: UserIdDep) -> List[Review]:
    return await service.get_reviews(query_params)


@router.delete('/{review_id}/delete', description='Удалить рецензию')
async def delete_review(review_id: UUID, service: ReviewServiceDep, _: UserIdDep):
    await service.delete_review(review_id)


@router.post('/{review_id}/assessment/like', description='Поставить лайк рецензии')
async def like_review(review_id: UUID, service: ReviewServiceDep,
                      user_id: UserIdDep):
    await service.add_assessment_to_review(review_id, user_id, True)


@router.post('/{review_id}/assessment/dislike', description='Поставить дизлайк рецензии')
async def dislike_review(review_id: UUID, service: ReviewServiceDep,
                         user_id: UserIdDep):
    await service.add_assessment_to_review(review_id, user_id, False)


@router.delete('/{review_id}/assessment/delete', description='Удалить оценку рецензии')
async def delete_assessment_review(review_id: UUID, service: ReviewServiceDep,
                                   user_id: UserIdDep):
    await service.delete_assessment_review(review_id, user_id)


@router.get('/{review_id}/assessment', description='Рейтинг рецензии')
async def get_rating_review(review_id: UUID, service: ReviewServiceDep,
                            _: UserIdDep) -> ReviewRating:
    return await service.get_review_rating(review_id)


@router.get('/daily-top-reviews', description='Самые популярные рецензии за день')
async def get_rating_review(service: ReviewServiceDep):
    return await service.get_daily_top_reviews()
