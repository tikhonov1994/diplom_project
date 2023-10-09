from abc import ABC, abstractmethod

import aio_pika


class EmailConsumerBase(ABC):
    @staticmethod
    @abstractmethod
    async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
        raise NotImplementedError
