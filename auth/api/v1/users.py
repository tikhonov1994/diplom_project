from uuid import UUID

from db.model import UserInfo
from fastapi import APIRouter, Depends, HTTPException
from schemas.role import PatchUserRoleSchema
from schemas.user import PatchUserInfoSchema
from starlette import status
from utils.auth import require_user

from services import (AuthServiceDep, ServiceItemNotFound,
                      ServiceUniqueFieldViolation, UserServiceDep)
from utils.auth import admin_required
from utils.tracer import inject_request_id

router = APIRouter()


@router.patch('/{user_id}/role',
              description='Установить роль для пользователя',
              dependencies=[Depends(inject_request_id)])
@admin_required
async def grant_role_to_user(user_id: UUID,
                             role_info: PatchUserRoleSchema,
                             service: UserServiceDep,
                             current_user: UserInfo = Depends(require_user)) -> None:
    try:
        await service.grant_role_to_user(user_id, role_info.role_id)
    except ServiceItemNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch('/credentials',
              description='Изменение данных пользователя',
              dependencies=[Depends(inject_request_id)])
async def update_credentials(auth_service: AuthServiceDep,
                             user_service: UserServiceDep,
                             changes: PatchUserInfoSchema,
                             _: UserInfo = Depends(require_user)) -> None:
    if not changes.email and not changes.password:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    try:
        user_id = await auth_service.get_user_id()
        await user_service.update_credentials(user_id, changes)
    except ServiceUniqueFieldViolation as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ServiceItemNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
