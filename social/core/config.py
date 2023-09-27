from typing import Optional

from pydantic import BaseSettings, Field

_ENV_FILE_LOC = '.env'


class SocialMongoConfig(BaseSettings):  # type: ignore
    host: str
    port: int

    @property
    def mongo_uri(self) -> str:
        return f'mongodb://{self.host}:{self.port}/{self.social_database}'

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'mongo_'


class SocialConfig(BaseSettings):  # type: ignore
    project_name: str
    host: str
    port: int
    log_level: str
    version: str = 'dev'
    logstash_port: int
    mongo_database: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'social_'


class LogstashConfig(BaseSettings):  # type: ignore
    host: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'logstash_'


class AppConfig(BaseSettings):  # type: ignore
    authjwt_secret_key: Optional[str] = Field(None, env='JWT_SECRET_KEY')
    sentry_dsn: str
    debug: bool
    export_logs: bool = False

    api: SocialConfig = SocialConfig()
    mongo: SocialMongoConfig = SocialMongoConfig()
    logstash: LogstashConfig = LogstashConfig()

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
