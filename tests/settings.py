from pydantic import BaseSettings


class TestSettings(BaseSettings):
    api_host: str
    api_port: int

    elastic_host: str
    elastic_port: int

    redis_host: str
    redis_port: str

    class Config:
        env_file = '../.env'


test_settings = TestSettings()

__all__ = ['test_settings']
