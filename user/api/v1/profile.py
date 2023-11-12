from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from core.auth import AuthorizedUserId
from schemas.profile import UserProfileSchema, UserProfileUpdateSchema
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from services import UserProfileServiceDep
from services.user_profile import (UserProfileServiceError, UserProfileNotFoundError,
                                   UserProfileAlreadyExistsError)

router = APIRouter()


@router.post('/create',
             description='Создать профиль пользователя')
async def create_profile(user_id: AuthorizedUserId,
                         data: UserProfileSchema,
                         service: UserProfileServiceDep) -> JSONResponse:
    try:
        await service.create_profile(data, user_id)
    except UserProfileAlreadyExistsError as err:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err.message)
    except UserProfileServiceError as err:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=err.message)

    return JSONResponse(status_code=HTTPStatus.OK,
                        content={'detail': 'User profile save successfully.'})


@router.patch('/update', description='Обновить профиль пользователя')
async def update_profile(user_id: AuthorizedUserId,
                         data: UserProfileUpdateSchema,
                         service: UserProfileServiceDep) -> JSONResponse:
    try:
        await service.update_profile(data, user_id)
    except UserProfileNotFoundError as err:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err.message)

    return JSONResponse(status_code=HTTPStatus.OK,
                        content={'detail': 'User profile save successfully.'})


@router.get('/get', description='Получить профиль пользователя')
async def get_profile(user_id: AuthorizedUserId,
                      token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
                      service: UserProfileServiceDep):
    try:
        return await service.get_profile(user_id, token.credentials)
    except UserProfileNotFoundError as err:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err.message)


@router.delete('/delete', description='Удалить профиль пользователя')
async def delete(user_id: AuthorizedUserId, service: UserProfileServiceDep) -> JSONResponse:
    try:
        await service.destroy_profile(user_id)
    except UserProfileNotFoundError as err:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err.message)

    return JSONResponse(status_code=HTTPStatus.OK,
                        content={'detail': 'User profile deleted successfully.'})
