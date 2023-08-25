from typing import Annotated
from pydantic import AnyHttpUrl
from fastapi import APIRouter, HTTPException, Request, Depends, Query
from schemas.auth import (HistoryListSchema, LoginSchema, RefreshSchema,
                          TokensSchema, HistorySchema, LoginResponseSchema)
from starlette import status
from db.model import UserInfo
from utils.auth import require_user

from services import (AuthServiceDep, ServiceUniqueFieldViolation,
                      UserServiceDep, YandexOauthDep)
from utils.tracer import inject_request_id

router = APIRouter()


@router.post(
    path='/login',
    description='Аутентификация юзера',
    response_model=LoginResponseSchema,
    dependencies=[Depends(inject_request_id)]
)
async def login(validated_data: LoginSchema,
                request: Request,
                service: AuthServiceDep) -> TokensSchema:
    return await service.login_by_password(validated_data.email, validated_data.password, request.headers.get('user-agent'))


@router.post('/refresh',
             description='Обновление токенов',
             response_model=TokensSchema,
             dependencies=[Depends(inject_request_id)])
async def refresh(validated_data: RefreshSchema, request: Request, service: AuthServiceDep) -> TokensSchema:
    result = await service.refresh(validated_data.refresh_token, request.headers.get('user-agent'))
    return result


@router.post('/register',
             description='Регистрация пользователя',
             dependencies=[Depends(inject_request_id)])
async def user_registration(user_service: UserServiceDep, auth_service: AuthServiceDep,
                            request: Request, validated_data: LoginSchema) -> TokensSchema:
    email, password = validated_data.email, validated_data.password
    try:
        await user_service.save_user(email, password)
    except ServiceUniqueFieldViolation as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    result = await auth_service.login_by_password(email, password, request.headers.get('user-agent'))

    return result


@router.delete('/logout',
               description='Выход из системы',
               status_code=status.HTTP_205_RESET_CONTENT,
               dependencies=[Depends(inject_request_id)])
async def logout(auth_service: AuthServiceDep,
                 _: UserInfo = Depends(require_user)) -> dict:
    await auth_service.logout()
    return {"detail": "Refresh token has been revoke"}


@router.get('/history',
            description='История входов в аккаунт',
            dependencies=[Depends(inject_request_id)])
async def get_history(auth_service: AuthServiceDep,
                      _: UserInfo = Depends(require_user),
                      page_size: Annotated[int, Query(gt=0, lt=10_000)] = 50,
                      page_number: Annotated[int, Query(gt=0)] = 1) -> HistoryListSchema:
    data = await auth_service.get_user_history()
    total_pages = data['count'] // page_size if data['count'] % page_size == 0 else (data['count'] // page_size + 1)
    if page_number > total_pages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Page number must be less total pages!')
    first_elem = page_number * page_size - page_size
    last_elem = page_number * page_size
    return HistoryListSchema(
        count=data['count'],
        total_pages=total_pages,
        prev=page_number - 1 if 1 < page_number <= (total_pages + 1) else None,
        next=(page_number + 1) if page_number < total_pages else None,
        results=[HistorySchema.parse_obj(item_obj) for item_obj in data['results'][first_elem:last_elem]]
    )


@router.get('/social_auth',
            description='Регистрация через социальные сети',
            dependencies=[Depends(inject_request_id)])
async def social_auth(yandex_oauth: YandexOauthDep, provider: str = 'yandex') -> AnyHttpUrl:
    if provider == 'yandex':
        return await yandex_oauth.get_authorization_url()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unknown provider!')


@router.get('/yandex/verification_code',
            description='Авторизации после входа через yandex',
            dependencies=[Depends(inject_request_id)])
async def verificate(code: str, yandex_oauth: YandexOauthDep,
                     auth_service: AuthServiceDep, request: Request) -> TokensSchema:
    user_info = await yandex_oauth.get_user_info(code)
    try:
        user = await yandex_oauth.get_or_create_user(user_info)
    except ServiceUniqueFieldViolation as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    return await auth_service.login(user, request.headers.get('user-agent'))


@router.delete('/delete_social',
               description='Открепление аккаунта от соцсети',
               dependencies=[Depends(inject_request_id)])
async def delete_social(auth_service: AuthServiceDep, yandex_oauth: YandexOauthDep,
                        _: UserInfo = Depends(require_user)) -> dict:
    user_id = await auth_service.get_user_id()
    await yandex_oauth.delete_user_social(user_id)
    return {"detail": "The link to the social network has been deleted"}
