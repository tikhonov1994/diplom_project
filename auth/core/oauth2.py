from async_fastapi_jwt_auth import AuthJWT

from core.config import app_config
from typing import List
from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_algorithm: str = app_config.jwt_algorithm
    authjwt_decode_algorithms: List[str] = [app_config.jwt_algorithm]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_secret_key: str = app_config.jwt_secret_key


@AuthJWT.load_config
def get_config():
    return Settings()
