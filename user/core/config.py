from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE_LOC = '.env'
_SECURE_ENV_FILE_LOC = '.env.secure'


class UserConfig(BaseSettings):  # type: ignore
    project_name: str
    host: str
    port: int
    log_level: str
    version: str = 'dev'
    logstash_port: int
    db_schema: str
    minio_image_bucket: str

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE_LOC,
        env_prefix='user_',
        extra='ignore'
    )


class LogstashConfig(BaseSettings):  # type: ignore
    host: str

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE_LOC,
        env_prefix='logstash_',
        extra='ignore'
    )


class SecurePostgresConfig(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    db: str
    driver: str

    @property
    def dsn(self) -> str:
        return f'postgresql+{self.driver}://{self.user}:{self.password}' \
               f'@{self.host}:{self.port}/{self.db}'

    model_config = SettingsConfigDict(
        env_file=_SECURE_ENV_FILE_LOC,
        env_prefix='postgres_',
        extra='ignore'
    )


class NsfwJSServiceConfig(BaseSettings):
    host: str
    port: str

    @property
    def url(self) -> str:
        return f'http://{self.host}:{self.port}/single/multipart-form'

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE_LOC,
        env_prefix='nsfwjs_',
        extra='ignore'
    )


class MinioConfig(BaseSettings):
    host: str
    port: int
    root_user: str
    root_password: str

    @property
    def endpoint(self) -> str:
        return f'{self.host}:{self.port}'

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE_LOC,
        env_prefix='minio_',
        extra='ignore'
    )


class AppConfig(BaseSettings):  # type: ignore
    authjwt_secret_key: Optional[str] = Field(None, env='JWT_SECRET_KEY')
    sentry_dsn: str
    debug: bool
    export_logs: bool = False
    enable_tracer: bool = False

    api: UserConfig = UserConfig()
    logstash: LogstashConfig = LogstashConfig()
    secure_db: SecurePostgresConfig = SecurePostgresConfig()
    nsfw: NsfwJSServiceConfig = NsfwJSServiceConfig()
    minio: MinioConfig = MinioConfig()

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE_LOC,
        extra='ignore',
    )


app_config = AppConfig()

__all__ = ['app_config']
