import os

from pydantic import BaseSettings


_ENV_FILE_LOC = '.env'


class ApiConfig(BaseSettings):
    project_name: str
    host: str
    port: int
    version: str = "0.0.1"

    cache_expire_seconds: int = 60
    logging_level: int = 20
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logstash_port: int

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'api_'


class LogstashConfig(BaseSettings):
    host: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'logstash_'


class SentryConfig(BaseSettings):
    dsn: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'sentry_'


class AppConfig(BaseSettings):
    # Logging
    log_level: str
    export_logs: bool = False

    # Service
    api: ApiConfig = ApiConfig()
    logstash: LogstashConfig = LogstashConfig()
    sentry: SentryConfig = SentryConfig()

    # Redis
    redis_host: str
    redis_port: int

    # Elastic
    elastic_host: str
    elastic_port: int

    # Token settings
    jwt_algorithm: str
    jwt_secret_key: str
    auth_token_expire_minutes: int
    refresh_token_expire_minutes: int

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
