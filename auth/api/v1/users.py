from uuid import UUID
from pydantic import EmailStr

from fastapi import APIRouter, HTTPException
from starlette import status

from schemas.role import PatchUserRoleSchema

from services import UserServiceDep, ServiceItemNotFound, UtilServiceDep

router = APIRouter()


@router.patch('/{user_id}/role', description='Установить роль для пользователя')
async def grant_role_to_user(
        user_id: UUID,
        role_info: PatchUserRoleSchema,
        service: UserServiceDep) -> None:
    try:
        await service.grant_role_to_user(user_id, role_info.role_id)
    except ServiceItemNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/register', description='Регистрация пользователя')
async def user_registration(user_service: UserServiceDep, email: EmailStr,
                            password: str, util_service: UtilServiceDep) -> bool:
    if await user_service.check_user_by_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User with email {email} already exists!')
    hashed_password = util_service.generate_hashed_password(password)
    await user_service.save_user(email, hashed_password)
    return True
