from uuid import UUID

from db.model import UserInfo
from fastapi import APIRouter, Depends, HTTPException
from schemas.role import AddUserRoleSchema, UserRoleSchema
from starlette import status
from utils.auth import require_user, admin_required

from services import (RoleServiceDep, ServiceConflictOnAddError,
                      ServiceConflictOnDeleteError, ServiceItemNotFound)

router = APIRouter()


@router.get('', response_model=list[UserRoleSchema], description='Получить список пользовтельских ролей')
@admin_required
async def roles_list(
        service: RoleServiceDep,
        current_user: UserInfo = Depends(require_user)) -> list[UserRoleSchema]:
    return await service.get_roles()


@router.post('', description='Добавить пользовательскую роль')
@admin_required
async def add_role(new_role: AddUserRoleSchema,
                   service: RoleServiceDep,
                   current_user: UserInfo = Depends(require_user)) -> None:
    try:
        await service.add_role(new_role.name)
    except ServiceConflictOnAddError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.delete('/{role_id}', description='Удалить пользовательскую роль')
@admin_required
async def delete_role(role_id: UUID,
                      service: RoleServiceDep,
                      current_user: UserInfo = Depends(require_user)) -> None:
    try:
        await service.delete_role(role_id)
    except ServiceItemNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ServiceConflictOnDeleteError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
