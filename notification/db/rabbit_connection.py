import json
import uuid

import aio_pika
from typing import Annotated  # type: ignore[attr-defined]

from aio_pika import connect_robust
from aio_pika.message import Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractRobustExchange, ExchangeType, \
    DeliveryMode
from fastapi import Depends
from schemas.notification import NotificationMessageSchema, NotificationRequestSchema



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
        try:
            # todo юрл вида "amqp://guest:guest@127.0.0.1/"
            # self._connection = await connect_robust(config.rabbit.dsn)
            # self._connection = await connect_robust('amqp://rmuser:rmpassword@rabbitmq/')
            self._connection = await connect_robust('amqp://rmuser:rmpassword@localhost/')
            self._channel = await self._connection.channel(publisher_confirms=False)
            # todo create exchange if not exists:
            self._exchange = await self._channel.declare_exchange(
                'test',
                # config.exchange_name, todo
                durable=True,
                # ExchangeType.X_DELAYED_MESSAGE,
                # arguments={
                #     'x-delayed-type': 'direct'
                # }
            )

            queue = await self._channel.declare_queue('test', exclusive=True)
            await queue.bind(self._exchange, routing_key='test') # todo
            print('successfully connected to rabbitmq exchange')
        except Exception as e:
            print('wtfffff')
            print(e)
            print('----------')
            await self.disconnect()

    async def send_messages(
            self,
            message_data: NotificationMessageSchema, # todo delete
            *,
            # routing_key: str = rabbit_config.RABBITMQ_QUEUE, todo пока хз где буду указывать биндинг
            routing_key: str = 'test',
            delay: int = None
    ) -> None:
        async with self._channel.transaction():
            headers = None
            # if delay:
            #     headers = {
            #         'x-delay': f'{delay * 1000}'
            #     }

            message = Message(
                # headers=headers
                body=json.dumps(message_data.dict()).encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
            )
            await self._exchange.publish(
                message,
                routing_key=routing_key,
            )


rabbit_connection = RabbitConnection()

