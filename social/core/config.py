from pydantic import BaseSettings, Field

_ENV_FILE_LOC = '.env'


class SocialMongoConfig(BaseSettings):
    host: str
    port: int
    social_database: str

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

    class Config:
        env_file = _ENV_FILE_LOC
        env_prefix = 'social_'


class AppConfig(BaseSettings):
    authjwt_secret_key: str = Field(None, env='JWT_SECRET_KEY')
    sentry_dsn: str

    api: SocialConfig = SocialConfig()
    mongo: SocialMongoConfig = SocialMongoConfig()

    class Config:
        env_file = _ENV_FILE_LOC


app_config = AppConfig()

__all__ = ['app_config']
