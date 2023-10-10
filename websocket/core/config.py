from typing import Optional

from pydantic import BaseSettings, Field

_ENV_FILE_LOC = '.env'


class WebsocketConfig(BaseSettings):  # type: ignore
    project_name: str
    host: str
    port: int

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'websocket_'


class AppConfig(BaseSettings):  # type: ignore
    authjwt_secret_key: Optional[str] = Field(None, env='JWT_SECRET_KEY')

    api: WebsocketConfig = WebsocketConfig()

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
