from typing import Type

from handlers.consumer_base import EmailConsumerBase
from handlers.simple_consumer import SimpleEmailConsumer


def sender_type() -> Type[EmailConsumerBase]:
    return SimpleEmailConsumer
