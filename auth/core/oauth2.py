from async_fastapi_jwt_auth import AuthJWT

from core.config import app_config
from typing import List
from pydantic import BaseModel
from db.redis import redis


class Settings(BaseModel):
    authjwt_algorithm: str = app_config.jwt_algorithm
    authjwt_decode_algorithms: List[str] = [app_config.jwt_algorithm]
    authjwt_token_location: set = {'headers'}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_secret_key: str = app_config.jwt_secret_key


@AuthJWT.load_config
def get_config():
    return Settings()


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    entry = redis.get(jti)
    return entry and entry == "true"
