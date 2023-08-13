from uuid import UUID
from pydantic import EmailStr

from fastapi import APIRouter, HTTPException, Request
from starlette import status
from schemas.auth import TokensSchema, HistorySchema

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


@router.post('/register', description='Регистрация пользователя', response_model=TokensSchema)
async def user_registration(user_service: UserServiceDep, email: EmailStr,
                            password: str, auth_service: AuthServiceDep,
                            request: Request):
    await user_service.save_user(email, password)
    result = await auth_service.login(email, password, request.headers.get('user-agent'))

    return result


@router.delete('/logout', description='Выход из системы')
async def logout(auth_service: AuthServiceDep) -> dict:
    await auth_service.logout()
    return {"detail": "Refresh token has been revoke"}


@router.get('/history', description='История входов в аккаунт', response_model=list[HistorySchema])
async def get_history(auth_service: AuthServiceDep):
    sessions = await auth_service.get_user_history()
    return [HistorySchema.parse_obj(item_obj) for item_obj in sessions]
