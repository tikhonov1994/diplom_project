from functools import wraps

from async_fastapi_jwt_auth.exceptions import MissingTokenError, RevokedTokenError
from core.oauth2 import AuthJWT
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from core.config import app_config
from db.model import UserInfo
from services import UserServiceDep

_bearer = HTTPBearer(auto_error=False)


async def require_user(user_service: UserServiceDep, _=Depends(_bearer),
                       authorize: AuthJWT = Depends()):
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
    except (MissingTokenError, RevokedTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth header is missing",
            headers={"Authorization": "Bearer"}
        )


def roles_required(roles_list: set[str]):
    def decorator(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            user: UserInfo = kwargs.get('current_user')
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Given credentials are invalid')
            if user.role.name not in roles_list:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail='This operation is forbidden')
            return await function(*args, **kwargs)

        return wrapper

    return decorator


admin_required = roles_required({app_config.api.admin_user_role, })
