import os

from pydantic import BaseSettings


_ENV_FILE_LOC = '.env'


class AuthConfig(BaseSettings):
    project_name: str
    host: str
    port: int

    cache_expire_seconds: int = 60
    logging_level: int = 20
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'auth_'


class AppConfig(BaseSettings):
    # Logging
    log_level: str

    # Service
    api: AuthConfig = AuthConfig()

    # Redis
    redis_host: str
    redis_port: int

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
