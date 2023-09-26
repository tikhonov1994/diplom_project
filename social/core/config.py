from pydantic import BaseSettings, Field

_ENV_FILE_LOC = '.env'


class SocialMongoConfig(BaseSettings):
    host: str
    port: int

    @property
    def mongo_uri(self) -> str:
        return f'mongodb://{self.host}:{self.port}/{self.social_database}'

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'mongo_'


class SocialConfig(BaseSettings):
    project_name: str
    host: str
    port: int
    log_level: str
    version: str = 'dev'
    logstash_port: int
    mongo_database: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'social_'


class LogstashConfig(BaseSettings):
    host: str

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'logstash_'


class AppConfig(BaseSettings):
    authjwt_secret_key: str = Field(None, env='JWT_SECRET_KEY')
    sentry_dsn: str
    debug: bool

    api: SocialConfig = SocialConfig()
    mongo: SocialMongoConfig = SocialMongoConfig()
    logstash: LogstashConfig = LogstashConfig()

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
