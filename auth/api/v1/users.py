from uuid import UUID
from pydantic import EmailStr

from fastapi import APIRouter, HTTPException, Request, Depends
from starlette import status
from schemas.auth import TokensSchema, HistorySchema

from schemas.role import PatchUserRoleSchema
from schemas.user import PatchUserInfoSchema

from services import UserServiceDep, ServiceItemNotFound, AuthServiceDep, ServiceUniqueFieldViolation
from utils.deps import require_user
from db.model import UserInfo

router = APIRouter()


@router.patch('/{user_id}/role', description='Установить роль для пользователя')
async def grant_role_to_user(
        user_id: UUID,
        role_info: PatchUserRoleSchema,
        service: UserServiceDep,
        user: UserInfo = Depends(require_user)) -> None:
    try:
        await service.grant_role_to_user(user_id, role_info.role_id)
    except ServiceItemNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post('/register', description='Регистрация пользователя', response_model=TokensSchema)
async def register_user(user_service: UserServiceDep, email: EmailStr,
                        password: str, auth_service: AuthServiceDep,
                        request: Request):
    try:
        await user_service.save_user(email, password)
        return await auth_service.login(email, password, request.headers.get('user-agent'))
    except ServiceUniqueFieldViolation as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.delete('/logout', description='Выход из системы', operation_id="authorize")
async def logout(auth_service: AuthServiceDep, user: UserInfo = Depends(require_user)) -> dict:
    await auth_service.logout()
    return {"detail": "Refresh token has been revoked"}


@router.patch('/credentials', description='Изменение данных пользователя')
async def update_credentials(auth_service: AuthServiceDep,
                             user_service: UserServiceDep,
                             changes: PatchUserInfoSchema) -> None:
    if not changes.email and not changes.password:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    try:
        user_id = await auth_service.get_user_id()
        await user_service.update_credentials(user_id, changes)
    except ServiceUniqueFieldViolation as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ServiceItemNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get('/history', description='История входов в аккаунт', response_model=list[HistorySchema])
async def get_history(auth_service: AuthServiceDep):
    sessions = await auth_service.get_user_history()
    return [HistorySchema.parse_obj(item_obj) for item_obj in sessions]
