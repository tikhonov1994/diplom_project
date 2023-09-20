from fastapi import APIRouter

from core.auth import UserIdDep
from schemas.reviews import ReviewSchema
from services import ReviewServiceDep

router = APIRouter()


@router.post('/')
async def send_review(validated_data: ReviewSchema,
                      service: ReviewServiceDep,
                      user_id: UserIdDep) -> dict:
    await service.add_review(validated_data.text, user_id, validated_data.film_id, validated_data.author_rating)
    return {'ok': True}
