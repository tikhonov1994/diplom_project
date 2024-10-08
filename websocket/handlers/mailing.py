from contextlib import asynccontextmanager
import json

import aio_pika

from adapters.rabbitmq import ConfiguredRabbitmq
from adapters.websocket import get_connection_manager
from core.config import app_config as cfg
from core.logger import get_logger
from schemas.mailing import MailingSchema, WebsocketMessageSchema

logger = get_logger()


async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process(ignore_processed=True, requeue=False):
        try:
            mailing = MailingSchema.model_validate(json.loads(message.body.decode()))
            _logger = get_logger(mailing.request_id)
            _logger.debug('New mailing [%s]: %s', message.message_id, message.body.decode())
            websocket = get_connection_manager()

            for recipient in mailing.recipients_list:
                msg = WebsocketMessageSchema(subject=mailing.subject,
                                             body=mailing.body,
                                             request_id=mailing.request_id)
                await websocket.send_message(msg, recipient)
        finally:
            await message.ack()


@asynccontextmanager
async def rabbitmq_consumer_task():
    rmq: ConfiguredRabbitmq = ConfiguredRabbitmq()
    await rmq.configure_broker()
    async with rmq.get_configured_channel() as channel:
        message_queue = await channel.get_queue(cfg.ws.queue_name)
        logger.info('Connected to %s, ready to handle messages!', cfg.rabbitmq.dsn)

        async def _task() -> None:
            await message_queue.consume(process_message)

        yield _task
        logger.info('Rabbitmq consumer is tearing down.')


__all__ = ['rabbitmq_consumer_task']
