from clickhouse_driver import Client

from src.core.config import app_config
from src.models import ViewsMessage


class ClickhouseViewsLoader:
    def __init__(self):
        self._client = Client(host=app_config.clickhouse.host,
                              port=app_config.clickhouse.port)

    def add_message(self, msg: ViewsMessage) -> None:
        self._client.execute(
            '''
            INSERT INTO ugc.views 
            SETTINGS async_insert=1, wait_for_async_insert=1 VALUES;
            ''',
            msg.dict()
        )
