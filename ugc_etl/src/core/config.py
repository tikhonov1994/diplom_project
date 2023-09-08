from pydantic import BaseSettings

_ENV_FILE_LOC = '../../../.env'


class KafkaConfig(BaseSettings):
    host: str
    port: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'kafka_'


class EtlConfig(BaseSettings):
    logging_level: int

    kafka: KafkaConfig = KafkaConfig()

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'ugc_etl_'


app_config = EtlConfig()

__all__ = ['app_config']
