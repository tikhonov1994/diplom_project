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
    user_agent = request.headers.get('user-agent')
    result = await service.login(validated_data.email, validated_data.password, user_agent)

    return result


# @router.post('/refresh')
# def refresh(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_refresh_token_required()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
#
    # todo закинуть старый токен
#     # todo текущий рефреш токен удалить/отключить
#     current_user = Authorize.get_jwt_subject()
#
#     new_access_token = Authorize.create_access_token(subject=current_user)
#     new_refresh_token = Authorize.create_refresh_token(subject=current_user)
#
#     # todo save to redis
#     return {"new_access_token": new_access_token}