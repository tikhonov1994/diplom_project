from fastapi import APIRouter, Request

from schemas.auth import TokensSchema
from services import AuthServiceDep

from schemas.auth import LoginSchema

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


@router.post('/refresh', description='Обновление токенов', response_model=TokensSchema)
async def refresh(refresh_token: str, request: Request, service: AuthServiceDep):
    result = await service.refresh(refresh_token, request.headers.get('user-agent'))

    return result
