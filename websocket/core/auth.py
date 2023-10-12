from typing import Annotated
from uuid import UUID

from fastapi import Depends, WebSocketException, Query
from jose import jwt

from core.config import app_config as cfg


async def get_user_id(access_token: str = Query()) -> UUID:
    try:
        payload = jwt.decode(access_token, cfg.jwt_secret_key, algorithms=["HS256"])

        return UUID(payload.get('sub'))
    except (KeyError, jwt.JWTError):
        raise WebSocketException(
            code=4001,
            reason='Bad auth credentials.'
        )


UserIdDep = Annotated[UUID, Depends(get_user_id)]
