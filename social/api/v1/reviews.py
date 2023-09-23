from uuid import UUID
from fastapi import APIRouter

from core.auth import UserIdDep
from schemas.reviews import ReviewSchema
from services import ReviewServiceDep
from models.review import Review, ReviewRating

router = APIRouter()


@router.post('/review/add', description='Отправить рецензию')
async def send_review(validated_data: ReviewSchema,
                      service: ReviewServiceDep,
                      user_id: UserIdDep) -> dict:
    await service.add_review(validated_data.text, user_id, validated_data.film_id, validated_data.author_rating)
    return {'ok': True}


@router.post('/review/{review_id}/edit', description='Изменить рецензию')
async def update_review(review_id: UUID, validated_data: ReviewSchema,
                        service: ReviewServiceDep,
                        user_id: UserIdDep):
    await service.update_review(validated_data.text, user_id, validated_data.author_rating,
                                validated_data.film_id, review_id)


@router.get('/review', description='Все рецензии')
async def all_reviews(service: ReviewServiceDep, _: UserIdDep) -> list[Review]:
    return await service.get_all_reviews()


@router.delete('/review/{review_id}/delete', description='Удалить рецензию')
async def delete_review(review_id: UUID, service: ReviewServiceDep, _: UserIdDep):
    await service.delete_review(review_id)


@router.post('/review/{review_id}/assessment/like', description='Поставить лайк рецензии')
async def like_review(review_id: UUID, service: ReviewServiceDep,
                      user_id: UserIdDep):
    await service.add_assessment_to_review(review_id, user_id, True)


@router.post('/review/{review_id}/assessment/dislike', description='Поставить дизлайк рецензии')
async def dislike_review(review_id: UUID, service: ReviewServiceDep,
                         user_id: UserIdDep):
    await service.add_assessment_to_review(review_id, user_id, False)


@router.delete('/review/{review_id}/assessment/delete', description='Удалить оценку рецензии')
async def delete_assessment_review(review_id: UUID, service: ReviewServiceDep,
                                   user_id: UserIdDep):
    await service.delete_assessment_review(review_id, user_id)


@router.get('/review/{review_id}/assessment', description='Рейтинг рецензии')
async def get_rating_review(review_id: UUID, service: ReviewServiceDep,
                            _: UserIdDep) -> ReviewRating:
    return await service.get_review_rating(review_id)
