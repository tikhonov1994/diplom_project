import aio_pika
import json

from handlers.consumer_base import EmailConsumerBase
from core.logger import logger
from schemas.mailing import Mailing


class SimpleEmailConsumer(EmailConsumerBase):
    @staticmethod
    async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
        # async with message.process():
        #     print(message.body)
        #     await asyncio.sleep(1)
        # ...
        async with message.process():
            logger.debug('New message: %s', message.body.decode())
            mailing = Mailing.model_validate(json.loads(message.body.decode()))

        pass
