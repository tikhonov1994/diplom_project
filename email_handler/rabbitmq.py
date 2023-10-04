from typing import Coroutine

import aio_pika

from core.config import app_config


def connect() -> Coroutine[any, any, aio_pika.abc.AbstractRobustConnection]:
    return aio_pika.connect_robust(app_config.rabbitmq.dsn)
