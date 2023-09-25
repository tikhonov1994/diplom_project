from pydantic import BaseSettings

_ENV_FILE_LOC = '.env'


class KafkaConfig(BaseSettings):
    host: str
    port: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'kafka_'


class ClickhouseConfig(BaseSettings):
    host: str
    port: str
    insert_batch_size: int = 10000
    insert_batch_timeout_sec: float = 1.

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'clickhouse_'


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


class EtlConfig(BaseSettings):
    log_filename: str
    logging_level: int
    logstash_port: int
    version: str = '0.0.1'

    topic_name: str = 'views'
    group_id: str = 'views_consumer_group'
    admin_client_id: str = 'views_admin_client'
    topic_replica_factor: int = 1
    topic_partitions_count: int = 1

    kafka: KafkaConfig = KafkaConfig()
    clickhouse: ClickhouseConfig = ClickhouseConfig()
    sentry: SentryConfig = SentryConfig()
    logstash: LogstashConfig = LogstashConfig()

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'ugc_etl_'


app_config = EtlConfig()

__all__ = ['app_config']
