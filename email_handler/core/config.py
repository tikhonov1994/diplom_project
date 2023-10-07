from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE_NAME = './.env'


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
        env_file=_ENV_FILE_NAME,
        extra='ignore')


class AuthServiceConfig(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_prefix='AUTH_',
        env_file=_ENV_FILE_NAME,
        extra='ignore')


class NotificationServiceConfig(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_prefix='NOTIFICATION_',
        env_file=_ENV_FILE_NAME,
        extra='ignore')


class EmailWorkerConfig(BaseSettings):
    version: str = '0.0.1'
    name: str = 'EmailHandler'
    queue_name: str
    prefetch_count: int = 4
    debug: bool = False
    logstash_port: int

    email_address: str
    email_password: str
    smtp_host: str
    smtp_port: int

    @property
    def smtp_connect_params(self) -> dict:
        return {'hostname': self.smtp_host,
                'port': self.smtp_port,
                'username': self.email_address,
                'password': self.email_password,
                'use_tls': True}

    model_config = SettingsConfigDict(
        env_prefix='EMAIL_HANDLER_',
        env_file=_ENV_FILE_NAME,
        extra='ignore')


class LogstashConfig(BaseSettings):
    host: str

    class Config:
        env_file = _ENV_FILE_NAME
        env_prefix = "logstash_"


class AppConfig(BaseSettings):
    export_logs: bool = False
    sentry_dsn: str

    rabbitmq: RabbitMqConfig = RabbitMqConfig()
    worker: EmailWorkerConfig = EmailWorkerConfig()
    logstash: LogstashConfig = LogstashConfig()
    auth: AuthServiceConfig = AuthServiceConfig()
    notification: NotificationServiceConfig = NotificationServiceConfig()

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE_NAME,
        extra='ignore')


app_config = AppConfig()

__all__ = ['app_config']
