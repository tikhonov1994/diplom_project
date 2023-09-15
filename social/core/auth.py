from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import MissingTokenError, RevokedTokenError

_bearer = HTTPBearer(auto_error=False)


async def get_user_id(_=Depends(_bearer), authorize: AuthJWT = Depends()):
    try:
        await authorize.jwt_required()
        user_id = await authorize.get_jwt_subject()

        return user_id
    except (MissingTokenError, RevokedTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth header is missing",
            headers={"Authorization": "Bearer"}
        )
