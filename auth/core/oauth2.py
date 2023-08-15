from typing import List

from async_fastapi_jwt_auth import AuthJWT
from core.config import app_config
from db.redis import get_redis
from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_algorithm: str = app_config.jwt_algorithm
    authjwt_decode_algorithms: List[str] = [app_config.jwt_algorithm]
    authjwt_token_location: set = {'headers'}
    authjwt_header_name: str = 'Authorization'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_secret_key: str = app_config.jwt_secret_key
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}


@AuthJWT.load_config
def get_config():
    return Settings()


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    redis = await get_redis()
    jti = decrypted_token["jti"]
    entry = await redis.get(jti)
    return entry and entry == b'true'
