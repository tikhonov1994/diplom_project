from pydantic import BaseSettings, Field

_ENV_FILE_LOC = '.env'


class RabbitMqConfig(BaseSettings):  # type: ignore
    host: str
    port: int = 5672
    default_user: str
    default_pass: str

    @property
    def dsn(self) -> str:
        return f'amqp://{self.default_user}:{self.default_pass}@{self.host}:{self.port}/'

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'rabbitmq_'


class NotificationConfig(BaseSettings):  # type: ignore
    project_name: str
    host: str
    port: int
    log_level: str
    version: str = 'dev'
    logstash_port: int
    db_schema: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'notification_'


class LogstashConfig(BaseSettings):  # type: ignore
    host: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'logstash_'


class AppConfig(BaseSettings):  # type: ignore
    sentry_dsn: str
    debug: bool
    export_logs: bool = False

    queue_name: str = Field(None, env='EMAIL_HANDLER_QUEUE_NAME')
    exchange_name: str = Field(None, env='EMAIL_HANDLER_EXCHANGE_NAME')

    api: NotificationConfig = NotificationConfig()
    rabbitmq: RabbitMqConfig = RabbitMqConfig()
    logstash: LogstashConfig = LogstashConfig()

    # Postgres
    postgres_host: str
    postgres_port: int
    postgres_driver: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    @property
    def postgres_dsn(self) -> str:
        return f'postgresql+{self.postgres_driver}://{self.postgres_user}:{self.postgres_password}' \
               f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
