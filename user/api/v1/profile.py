from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from core.auth import AuthorizedUserId
from schemas.profile import UserProfileSchema
from services import UserProfileServiceDep

router = APIRouter()


@router.post('/create',
             description='Создать профиль пользователя')
async def create_profile(user_id: AuthorizedUserId,
                         data: UserProfileSchema,
                         service: UserProfileServiceDep) -> JSONResponse:
    await service.create_profile(data, user_id)

    return JSONResponse(status_code=HTTPStatus.OK,
                        content={'detail': 'User profile save successfully.'})


@router.patch('/update', description='Обновить профиль пользователя')
async def update_profile(user_id: AuthorizedUserId,
                         data: UserProfileSchema,
                         service: UserProfileServiceDep) -> JSONResponse:
    await service.update_user(data, user_id)

    return JSONResponse(status_code=HTTPStatus.OK,
                        content={'detail': 'User profile save successfully.'})


@router.get('/get', description='Получить профиль пользователя')
async def get_profile(user_id: AuthorizedUserId,
                      service: UserProfileServiceDep) -> JSONResponse:
    await service.get_profile(user_id)

    return JSONResponse(status_code=HTTPStatus.OK,
                        content={'detail': 'User profile save successfully.'})


@router.delete('/{user_id}/delete', description='Удалить профиль пользователя')
async def delete(user_id: AuthorizedUserId, service: UserProfileServiceDep) -> JSONResponse:
    await service.destroy_profile(user_id)

    return JSONResponse(status_code=HTTPStatus.OK,
                        content={'detail': 'User profile deleted successfully.'})
