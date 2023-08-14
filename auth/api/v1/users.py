from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from schemas.role import PatchUserRoleSchema

from services import UserServiceDep, ServiceItemNotFound, AuthServiceDep

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
