from uuid import UUID
from pydantic import EmailStr
import time

from fastapi import APIRouter, HTTPException, Request
from starlette import status
from schemas.auth import TokensSchema
from async_fastapi_jwt_auth.exceptions import JWTDecodeError

from schemas.role import PatchUserRoleSchema

from services import UserServiceDep, ServiceItemNotFound, AuthServiceDep
from services.utils import generate_hashed_password
from db.redis import redis

router = APIRouter()


@router.patch('/{user_id}/role', description='Установить роль для пользователя')
async def grant_role_to_user(
        user_id: UUID,
        role_info: PatchUserRoleSchema,
        service: UserServiceDep) -> None:
    try:
        await service.grant_role_to_user(user_id, role_info.role_id)
    except ServiceItemNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post('/register', description='Регистрация пользователя', response_model=TokensSchema)
async def user_registration(user_service: UserServiceDep, email: EmailStr,
                            password: str, auth_service: AuthServiceDep,
                            request: Request):
    if await user_service.check_user_by_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User with email {email} already exists!')
    hashed_password = generate_hashed_password(password)
    await user_service.save_user(email, hashed_password)
    result = await auth_service.login(email, password, request.headers.get('user-agent'))

    return result


@router.delete('/logout', description='Выход из системы')
async def logout(auth_service: AuthServiceDep) -> dict:
    try:
        await auth_service.Authorize.jwt_required()
    except JWTDecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')
    decrypted_token = await auth_service.Authorize.get_raw_jwt()
    jti = decrypted_token['jti']
    refresh_jti = decrypted_token['refresh_jti']
    user_session = await auth_service.get_session_by_jti(refresh_jti)
    refresh_exp = (await auth_service.Authorize.get_raw_jwt(user_session.refresh_token))['exp']
    redis.setex(jti, (decrypted_token['exp'] - int(time.time())), 'true')
    redis.setex(refresh_jti, (refresh_exp - int(time.time())), 'true')
    await auth_service.close_session(user_session)
    return {"detail": "Refresh token has been revoke"}
