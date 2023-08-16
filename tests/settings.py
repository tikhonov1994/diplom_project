from pydantic import BaseSettings


class TestSettings(BaseSettings):
    api_host: str
    api_port: int

    auth_host: str
    auth_port: int

    elastic_host: str
    elastic_port: int

    redis_host: str
    redis_port: str

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_driver: str
    auth_db_schema: str
    default_user_role: str = 'user'
    admin_user_role: str = 'admin'

    # Token settings
    jwt_algorithm: str
    jwt_secret_key: str

    @property
    def postgres_dsn(self) -> str:
        return f'postgresql+{self.postgres_driver}://{self.postgres_user}:{self.postgres_password}' \
               f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    class Config:
        env_file = '../.env'


test_settings = TestSettings()

__all__ = ['test_settings']
