from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from core.config import app_config as cfg

scheme = HTTPBearer()


async def get_user_id(token: Annotated[HTTPAuthorizationCredentials, Depends(scheme)]) -> UUID:
    try:
        payload = jwt.decode(token=token.credentials,
                             key=cfg.jwt_secret_key,
                             algorithms=[cfg.jwt_algorithm])
        return UUID(payload.get('sub'))
    except (KeyError, jwt.JWTError):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Bad auth credentials.'
        )


AuthorizedUserId = Annotated[UUID, Depends(get_user_id)]

__all__ = ['AuthorizedUserId']
