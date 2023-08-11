from fastapi import APIRouter, Request

from schemas.auth import TokensSchema
from services import RoleServiceDep, AuthServiceDep, ServiceItemNotFound, ServiceConflictOnDeleteError, ServiceConflictOnAddError

from auth.schemas.auth import LoginSchema

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
