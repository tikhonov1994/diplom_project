from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE_LOC = '.env'


class KafkaConfig(BaseSettings):
    host: str
    port: str
    model_config = SettingsConfigDict(env_file=_ENV_FILE_LOC, env_prefix='kafka_')


class ClickhouseConfig(BaseSettings):
    host: str
    port: str
    insert_batch_size: int = 10000
    insert_batch_timeout_sec: float = 1.
    model_config = SettingsConfigDict(env_file=_ENV_FILE_LOC, env_prefix='clickhouse_')


class EtlConfig(BaseSettings):
    log_filename: str
    logging_level: int

    topic_name: str = 'views'
    group_id: str = 'views_consumer_group'
    admin_client_id: str = 'views_admin_client'
    topic_replica_factor: int = 1
    topic_partitions_count: int = 1

    kafka: KafkaConfig = KafkaConfig()
    clickhouse: ClickhouseConfig = ClickhouseConfig()
    model_config = SettingsConfigDict(env_file=_ENV_FILE_LOC, env_prefix='ugc_etl_')


app_config = EtlConfig()

__all__ = ['app_config']
