from fastapi import Depends, HTTPException, status, Request
from services import UserServiceDep
from core.oauth2 import AuthJWT


async def require_user(
        request : Request, user_service: UserServiceDep, Authorize: AuthJWT = Depends()):
    try:
        token = request.headers.get("jwt-token")
        await Authorize._verifying_token(token)
        # await Authorize.jwt_required()
    except Exception as e:
        kek = 'wqe'
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is expired",
        )

    user_id = await Authorize.get_jwt_subject()
    kek = ''
    current_user = await user_service.get_user_info(user_id)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with passed credentials not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user
