import aio_pika
import asyncio
from contextlib import asynccontextmanager

from core.config import app_config as cfg

_CONN_POOL_SIZE = 2
_CHANNEL_POOL_SIZE = 10


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


class ConfiguredRabbitmqChannel:
    def __init__(self, channel: aio_pika.abc.AbstractRobustChannel) -> None:
        self._channel = channel

    async def get_queue(self, queue_name: str) -> aio_pika.abc.AbstractQueue:
        return await self._channel.get_queue(queue_name, ensure=True)

    async def get_exchange(self, exchange_name: str) -> aio_pika.abc.AbstractExchange:
        return await self._channel.get_exchange(exchange_name, ensure=True)

    @property
    def get_default_exchange(self) -> aio_pika.abc.AbstractExchange:
        return self._channel.default_exchange


@singleton
class ConfiguredRabbitmq:
    def __init__(self) -> None:
        async def _get_connection() -> aio_pika.abc.AbstractRobustConnection:
            return await aio_pika.connect_robust(cfg.rabbitmq.dsn)

        self._conn_pool = aio_pika.pool.Pool(
            _get_connection,
            max_size=_CONN_POOL_SIZE,
            loop=asyncio.get_running_loop()
        )

        async def get_channel() -> aio_pika.Channel:
            async with self._conn_pool.acquire() as connection:
                return await connection.channel()

        self._channel_pool = aio_pika.pool.Pool(get_channel, max_size=_CHANNEL_POOL_SIZE,
                                                loop=asyncio.get_running_loop())

    @asynccontextmanager
    async def get_configured_channel(self) -> ConfiguredRabbitmqChannel:
        async with self._channel_pool.acquire() as _channel:
            yield ConfiguredRabbitmqChannel(_channel)

    async def configure_broker(self) -> None:
        async with self._channel_pool.acquire() as _channel:
            _queue: aio_pika.abc.AbstractRobustQueue = await _channel.declare_queue(
                cfg.worker.queue_name,
                durable=True

            )

            _queue_dl: aio_pika.abc.AbstractRobustQueue = await _channel.declare_queue(
                cfg.worker.dl_queue_name,
                durable=True
            )

            _exchange = await _channel.declare_exchange(
                cfg.worker.exchange_name,
                durable=True,
                type=aio_pika.ExchangeType.DIRECT
            )

            await _queue.bind(_exchange, routing_key=cfg.worker.routing_key)
            await _queue_dl.bind(_exchange, routing_key=cfg.worker.dl_routing_key)


__all__ = ['ConfiguredRabbitmq']
