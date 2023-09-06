import os

from pydantic import BaseSettings


_ENV_FILE_LOC = '.env'


class UgcConfig(BaseSettings):
    project_name: str
    host: str
    port: int

    logging_level: int = 20
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'ugc_'


class AppConfig(BaseSettings):
    # Logging
    log_level: str

    # Service
    api: UgcConfig = UgcConfig()

    # Kafka
    kafka_host: str
    kafka_port: int

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
