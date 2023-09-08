from clickhouse_driver import Client

from src.core.config import app_config
from src.models import ViewsMessage


class ClickhouseViewsLoader:
    def __init__(self):
        self._client = Client(host=app_config.clickhouse.host,
                              port=app_config.clickhouse.port)
        self.migrate()

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

    def add_message(self, msg: ViewsMessage) -> None:
        self._client.execute('INSERT INTO ugc.views SETTINGS async_insert=1, wait_for_async_insert=1 VALUES',
                             [msg.dict(),])
        print(self._client.execute('SELECT count(*) from ugc.views;'))
