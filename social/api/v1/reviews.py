from fastapi import APIRouter, Depends
from uuid import UUID

from core.auth import get_user_id
from schemas.reviews import ReviewSchema


router = APIRouter()


@router.post()
async def send_review(validated_date: ReviewSchema, user_id=Depends(get_user_id)):
    pass
