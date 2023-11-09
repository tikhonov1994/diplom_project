from http import HTTPStatus

from fastapi import APIRouter

from core.auth import UserIdDep
from services import UserGradeServiceDep

router = APIRouter()


@router.get('/',
            description='Get user social grade.',
            status_code=HTTPStatus.OK)
async def get_user_grade(user_id: UserIdDep,
                         service: UserGradeServiceDep) -> None:
    return await service.get_user_social_grade(user_id)
