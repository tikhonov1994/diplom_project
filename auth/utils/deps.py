from fastapi import Depends, HTTPException, status
from services import UserServiceDep
from core.oauth2 import AuthJWT


async def require_user(user_service: UserServiceDep, Authorize: AuthJWT = Depends()):
    try:
        await Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is expired",
        )

    # todo проверить что access токен не лежит в redis(т.е. не было логаута)

    user_id = await Authorize.get_jwt_subject()
    current_user = user_service.get_user_info(user_id)

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with passed credentials not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user
