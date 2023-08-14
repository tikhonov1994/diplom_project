from fastapi import APIRouter, Request

from schemas.auth import TokensSchema
from services import RoleServiceDep, UserServiceDep, AuthServiceDep, ServiceItemNotFound, ServiceConflictOnDeleteError, ServiceConflictOnAddError

from schemas.auth import LoginSchema, HistorySchema

router = APIRouter()


@router.post(
    path='/login',
    description='Аутентификация юзера',
    response_model=TokensSchema
)
async def login(
    validated_data: LoginSchema,
    request: Request,
    service: AuthServiceDep,
):
    result = await service.login(validated_data.email, validated_data.password, request.headers.get('user-agent'))

    return result


@router.post('/register', description='Регистрация пользователя', response_model=TokensSchema)
async def user_registration(user_service: UserServiceDep, auth_service: AuthServiceDep,
                            request: Request, validated_data: LoginSchema):
    email, password = validated_data.email, validated_data.password
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
