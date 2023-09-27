from pydantic import BaseSettings

_ENV_FILE_LOC = '../.env'


class PgConfig(BaseSettings):
    host: str
    port: int
    db: str
    user: str
    password: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'postgres_'

    @property
    def dsl(self) -> dict[str: any]:
        _dsl = self.dict()
        _dsl.pop('db')
        return _dsl | {'dbname': self.db}


class ElasticConfig(BaseSettings):
    host: str
    port: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'elastic_'


class LogstashConfig(BaseSettings):
    host: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = "logstash_"


class EtlConfig(BaseSettings):
    state_storage_name: str
    log_filename: str
    logging_level: int
    pg: PgConfig = PgConfig()
    version: str = "0.0.1"
    elastic: ElasticConfig = ElasticConfig()
    logstash: LogstashConfig = LogstashConfig()
    logstash_port: int

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'etl_'


app_config = EtlConfig()

__all__ = ['app_config']
