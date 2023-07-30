import abc
from decorators import coroutine
from typing import Generator


class BaseExtractor(abc.ABC):
    """Абстрактный экстрактор

    Позволяет доставать данные из БД Postgres.
    """

    BATCH_SIZE = 100

    def __init__(self, connection, table_name: str):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = table_name

    @abc.abstractmethod
    @coroutine
    def produce(self, next_node: Generator):
        pass
