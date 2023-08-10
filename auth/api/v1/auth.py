from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

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


@router.post('/refresh',
             description='Обновление токена',
             response_model=TokensSchema)
async def refresh(refresh_token : str, request: Request, service: AuthServiceDep):
    result = await service.refresh(refresh_token, request.headers.get('user-agent'))

    return result