import os

from pydantic import BaseSettings

_ENV_FILE_LOC = '.env'


class AuthConfig(BaseSettings):
    project_name: str
    host: str
    port: int
    db_schema: str
    admin_email: str
    admin_password: str
    default_user_role: str = 'user'
    admin_user_role: str = 'admin'

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
    debug: bool = False

    # Redis
    redis_host: str
    redis_port: int

    # Postgres
    postgres_host: str
    postgres_port: int
    postgres_driver: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    # Jaeger
    jaeger_host: str
    jaeger_port: int

    # Token settings
    jwt_algorithm: str
    jwt_secret_key: str
    auth_token_expire_minutes: int
    refresh_token_expire_minutes: int

    # OAuth
    yandex_client_id: str
    yandex_client_secret: str
    yandex_client_redirect_uri: str

    @property
    def postgres_dsn(self) -> str:
        return f'postgresql+{self.postgres_driver}://{self.postgres_user}:{self.postgres_password}' \
               f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
