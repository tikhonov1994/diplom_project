import os

from pydantic import BaseSettings


_ENV_FILE_LOC = '.env'


class UgcConfig(BaseSettings):  # type: ignore
    project_name: str
    host: str
    port: int
    version: str = '0.0.1'

    logstash_port: int
    logging_level: int = 20
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'ugc_'


class LogstashConfig(BaseSettings):  # type: ignore
    host: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'logstash_'


class SentryConfig(BaseSettings):  # type: ignore
    dsn: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'sentry_'


class AppConfig(BaseSettings):  # type: ignore
    # Logging
    log_level: str
    export_logs: bool = False
    jwt_secret_key: str
    jwt_algorithm: str

    # Service
    api: UgcConfig = UgcConfig()
    logstash: LogstashConfig = LogstashConfig()
    sentry: SentryConfig = SentryConfig()

    # Kafka
    kafka_host: str
    kafka_port: int

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
