from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError
from time import monotonic

from src.core.config import app_config
from src.models import ViewsMessage
from src.utils.backoff import backoff
from src.core.logger import logger


class ClickhouseViewsLoader:
    def __init__(self):
        self._client = Client(host=app_config.clickhouse.host,
                              port=app_config.clickhouse.port)
        self.migrate()
        self._batch_buffer: list[dict[str, any]] = []
        self._batch_time: float = monotonic()

    @backoff(exceptions=(NetworkError, EOFError))
    def migrate(self):
        self._client.execute('CREATE DATABASE IF NOT EXISTS ugc;')
        self._client.execute(
            '''CREATE TABLE IF NOT EXISTS ugc.views
                (
                    id UUID, 
                    movie_id UUID,
                    user_id UUID,
                    ts Int32,
                    created Int64
                ) Engine=MergeTree() ORDER BY created;'''
        )
        logger.info('ClickHouse migrated!')

    @backoff(exceptions=(NetworkError, EOFError))
    def add_message(self, msg: ViewsMessage) -> None:
        self._batch_buffer.append(msg.dict())

        if len(self._batch_buffer) > app_config.clickhouse.insert_batch_size \
                or (monotonic() - self._batch_time) > app_config.clickhouse.insert_batch_timeout_sec:

            if not self._batch_buffer:
                logger.info('No new items for clickhouse.')
                self._batch_time = monotonic()
                return

            self._client.execute('INSERT INTO ugc.views SETTINGS async_insert=1, wait_for_async_insert=1 VALUES',
                                 self._batch_buffer)
            logger.info('Loader buffer flush: pushed %d items to clickhouse.', len(self._batch_buffer))
            self._batch_time = monotonic()
            self._batch_buffer.clear()
