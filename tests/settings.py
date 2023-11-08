from pydantic import BaseSettings


class TestSettings(BaseSettings):
    api_host: str
    api_port: int

    auth_host: str
    auth_port: int

    ugc_host: str
    ugc_port: int

    social_host: str
    social_port: int
    social_mongo_database: str

    notification_host: str
    notification_port: int
    notification_db_schema: str

    user_host: str
    user_port: int
    user_minio_image_bucket: str

    elastic_host: str
    elastic_port: int

    redis_host: str
    redis_port: str

    mongo_host: str
    mongo_port: int

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_driver: str
    auth_db_schema: str
    default_user_role: str = 'user'
    admin_user_role: str = 'admin'

    minio_host: str
    minio_port: int
    minio_root_user: str
    minio_root_password: str

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
