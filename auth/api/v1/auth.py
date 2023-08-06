from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

from starlette.responses import JSONResponse

from schemas.auth import Tokens
from services import RoleServiceDep, AuthServiceDep, ServiceItemNotFound, ServiceConflictOnDeleteError, ServiceConflictOnAddError

router = APIRouter()

# todo сгенерить и положить в енв и конфиг
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post(
    path='/login',
    description='Аутентификация юзера',
    # response_model=Tokens
)
async def login(
    # form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: LoginRequest,
    # email: str,
    # password: str,
    service: AuthServiceDep,
):
    result = await service.login(request.email, request.password)

    return result


# @router.post('/refresh')
# def refresh(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_refresh_token_required()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
#
#     # todo текущий рефреш токен удалить/отключить
#     current_user = Authorize.get_jwt_subject()
#
#     new_access_token = Authorize.create_access_token(subject=current_user)
#     new_refresh_token = Authorize.create_refresh_token(subject=current_user)
#
#     # todo save to redis
#     return {"new_access_token": new_access_token}