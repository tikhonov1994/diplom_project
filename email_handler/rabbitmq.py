import aio_pika

from core.config import app_config

__connection = None


async def connect() -> aio_pika.abc.AbstractRobustConnection:
    global __connection
    if not __connection:
        __connection = await aio_pika.connect_robust(app_config.rabbitmq.dsn)
    return __connection


__all__ = ['connect']
