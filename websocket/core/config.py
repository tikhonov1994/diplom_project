from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE_LOC = '.env'


class RabbitMqConfig(BaseSettings):
    host: str
    port: int = 5672
    default_user: str
    default_pass: str

    @property
    def dsn(self) -> str:
        return f'amqp://{self.default_user}:{self.default_pass}@{self.host}:{self.port}/'

    model_config = SettingsConfigDict(
        env_prefix='RABBITMQ_',
        env_file=_ENV_FILE_LOC,
        extra='ignore')


class LogstashConfig(BaseSettings):
    host: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = "logstash_"


class WebsocketConfig(BaseSettings):
    version: str = '0.0.1'
    project_name: str = 'WebsocketHandler'
    host: str
    port: int
    debug: bool = False
    logstash_port: int

    # rabbitmq-related:
    queue_name: str
    exchange_name: str
    routing_key: str
    prefetch_count: int = 4

    model_config = SettingsConfigDict(
        env_prefix='WEBSOCKET_',
        env_file=_ENV_FILE_LOC,
        extra='ignore'
    )


class AppConfig(BaseSettings):
    export_logs: bool = False
    sentry_dsn: str

    jwt_secret_key: str

    ws: WebsocketConfig = WebsocketConfig()
    rabbitmq: RabbitMqConfig = RabbitMqConfig()
    logstash: LogstashConfig = LogstashConfig()

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE_LOC,
        extra='ignore'
    )


app_config = AppConfig()

__all__ = ['app_config']
