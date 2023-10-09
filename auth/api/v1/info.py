from uuid import UUID

from fastapi import APIRouter

from services import UserServiceDep
from schemas.user import UserInfoSchema

router = APIRouter()


@router.get('/{user_id}',
            description='Получение данных пользователя по его id',
            response_model=UserInfoSchema,
            include_in_schema=False)
async def get_user_info(user_id: UUID,
                        service: UserServiceDep) -> UserInfoSchema:
    return await service.get_user_info(user_id)
