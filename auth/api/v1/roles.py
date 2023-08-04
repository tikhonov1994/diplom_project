from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from schemas.role import UserRoleSchema, AddUserRoleSchema
from services import RoleServiceDep, ServiceItemNotFound, ServiceConflictOnDeleteError, ServiceConflictOnAddError

router = APIRouter()


@router.get('', response_model=list[UserRoleSchema], description='Получить список пользовтельских ролей')
async def roles_list(service: RoleServiceDep) -> list[UserRoleSchema]:
    return await service.get_roles()


@router.post('', description='Добавить пользовательскую роль')
async def add_role(new_role: AddUserRoleSchema, service: RoleServiceDep) -> None:
    try:
        await service.add_role(new_role.name)
    except ServiceConflictOnAddError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.delete('/{role_id}', description='Удалить пользовательскую роль')
async def delete_role(role_id: UUID, service: RoleServiceDep) -> None:
    try:
        await service.delete_role(role_id)
    except ServiceItemNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ServiceConflictOnDeleteError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
