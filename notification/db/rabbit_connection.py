import json
from typing import Annotated  # type: ignore[attr-defined]
from aio_pika import connect_robust
from aio_pika.message import Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractRobustExchange, ExchangeType, \
    DeliveryMode
from schemas.mailing import MailingMessageSchema
from core.config import app_config


class RabbitConnection:
    _connection: AbstractRobustConnection | None = None
    _channel: AbstractRobustChannel | None = None
    _exchange: AbstractRobustExchange | None = None

    async def disconnect(self) -> None:
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None

    async def connect(self) -> None:
        self._connection = await connect_robust(app_config.rabbitmq.dsn)
        self._channel = await self._connection.channel(publisher_confirms=False)
        self._exchange = await self._channel.declare_exchange(
            app_config.exchange_name,
            durable=True,
        )

        queue = await self._channel.declare_queue(app_config.queue_name, durable=True, exclusive=True)
        await queue.bind(self._exchange, routing_key='test')

    async def send_messages(
            self,
            message_data: MailingMessageSchema,
            *,
            routing_key: str = 'test',
    ) -> None:
        async with self._channel.transaction():
            message = Message(
                body=json.dumps(message_data.dict()).encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
            )
            await self._exchange.publish(
                message,
                routing_key=routing_key,
            )


rabbit_connection = RabbitConnection()

