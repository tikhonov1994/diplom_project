from async_fastapi_jwt_auth.exceptions import MissingTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from core.oauth2 import AuthJWT
from services import UserServiceDep


_bearer = HTTPBearer()


async def require_user(user_service: UserServiceDep, _ = Depends(_bearer), authorize: AuthJWT = Depends()):
    try:
        await authorize.jwt_required()
        user_id = await authorize.get_jwt_subject()
        current_user = await user_service.get_user_info(user_id)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User with passed credentials not found",
                headers={"Authorization": "Bearer"}
            )

        return current_user
    except MissingTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth header is missing",
            headers={"Authorization": "Bearer"}
        )
