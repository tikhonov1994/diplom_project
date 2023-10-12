from abc import ABC, abstractmethod

import aio_pika


class EmailConsumerBase(ABC):
    @classmethod
    @abstractmethod
    async def process_message(cls, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        raise NotImplementedError
