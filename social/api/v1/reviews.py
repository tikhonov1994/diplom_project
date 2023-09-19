from fastapi import APIRouter, Depends
from uuid import UUID

from core.auth import get_user_id
from schemas.reviews import ReviewSchema
from services import ReviewServiceDep


router = APIRouter()


@router.post('/')
async def send_review(validated_data: ReviewSchema, service: ReviewServiceDep,
                      user_id=Depends(get_user_id)) -> dict:
    await service.add_review(validated_data.text, user_id, validated_data.film_id, validated_data.author_rating)
    return {'ok': True}
