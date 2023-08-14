from typing import Annotated
from datetime import datetime

from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import app_config as config
from models.user import CurrentUser

oauth2_schema = HTTPBearer()


class AuthExceptionBase(Exception):
    pass


class TokenDecodeError(AuthExceptionBase):
    def __str__(self) -> str:
        return 'Failed to decode auth token'


class TokenExpiredError(AuthExceptionBase):
    def __str__(self) -> str:
        return 'Token expired'


class TokenFormatError(AuthExceptionBase):
    def __str__(self) -> str:
        return 'Token format is invalid'


def decode_token(token: HTTPAuthorizationCredentials) -> dict:
    return jwt.decode(token.credentials,
                      config.jwt_secret_key,
                      algorithms=config.jwt_algorithm,
                      options={'verify_exp': False})


def valid_access_token(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_schema)]) -> dict:
    try:
        token_payload = decode_token(token)
        if datetime.fromtimestamp(token_payload['exp']) < datetime.now():
            raise TokenExpiredError
        return token_payload
    except JWTError:
        raise TokenDecodeError


def current_user(valid_token: Annotated[dict, Depends(valid_access_token)]) -> CurrentUser:
    try:
        return CurrentUser.parse_obj(valid_token)
    except KeyError:
        raise TokenFormatError


UserRequiredDep = Annotated[CurrentUser, Depends(current_user)]

__all__ = ['UserRequiredDep']
