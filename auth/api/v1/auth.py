from async_fastapi_jwt_auth.exceptions import RevokedTokenError
from fastapi import APIRouter, HTTPException, Request
from schemas.auth import (HistorySchema, LoginSchema, RefreshSchema,
                          TokensSchema)
from starlette import status

from services import (AuthServiceDep, ServiceUniqueFieldViolation,
                      UserServiceDep)

router = APIRouter()


@router.post(
    path='/login',
    description='Аутентификация юзера',
    response_model=TokensSchema
)
async def login(validated_data: LoginSchema,
                request: Request,
                service: AuthServiceDep) -> TokensSchema:
    return await service.login(validated_data.email, validated_data.password, request.headers.get('user-agent'))


@router.post('/refresh', description='Обновление токенов', response_model=TokensSchema)
async def refresh(validated_data: RefreshSchema, request: Request, service: AuthServiceDep) -> TokensSchema:
    try:
        result = await service.refresh(validated_data.refresh_token, request.headers.get('user-agent'))
    except RevokedTokenError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)

    return result


@router.post('/register', description='Регистрация пользователя')
async def user_registration(user_service: UserServiceDep, auth_service: AuthServiceDep,
                            request: Request, validated_data: LoginSchema) -> TokensSchema:
    email, password = validated_data.email, validated_data.password
    try:
        await user_service.save_user(email, password)
    except ServiceUniqueFieldViolation as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    result = await auth_service.login(email, password, request.headers.get('user-agent'))

    return result


@router.delete('/logout', description='Выход из системы', status_code=status.HTTP_205_RESET_CONTENT)
async def logout(auth_service: AuthServiceDep) -> dict:
    try:
        await auth_service.logout()
    except RevokedTokenError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)
    return {"detail": "Refresh token has been revoke"}


@router.get('/history', description='История входов в аккаунт')
async def get_history(auth_service: AuthServiceDep) -> list[HistorySchema]:
    try:
        sessions = await auth_service.get_user_history()
    except RevokedTokenError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)
    return [HistorySchema.parse_obj(item_obj) for item_obj in sessions]
