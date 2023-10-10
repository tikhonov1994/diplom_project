from typing import Annotated  # type: ignore[attr-defined]
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import (MissingTokenError,
                                               RevokedTokenError)
from fastapi import Depends, HTTPException, status, Query


async def get_user_id(token: str = Query(...), authorize: AuthJWT = Depends()) -> UUID:
    try:
        await authorize.jwt_required("websocket", token=token)
        user_id = await authorize.get_jwt_subject()

        return UUID(user_id)
    except (MissingTokenError, RevokedTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth header is missing",
            headers={"Authorization": "Bearer"}
        )


UserIdDep = Annotated[UUID, Depends(get_user_id)]
