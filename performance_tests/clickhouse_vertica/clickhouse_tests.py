from time import monotonic
import multiprocessing as mp

from clickhouse_driver import Client

from test_base import TestBase
from test_data_source import get_test_records

CLICKHOUSE_HOST = 'localhost'


# noinspection SqlNoDataSourceInspection
class ClickhouseTests(TestBase):
    READ_QUERY = 'select distinct user_id from docker.test where ts > 2400;'

    def __init__(self, pre_filled_rec_count: int, cold_init: bool = True):
        if cold_init:
            client = Client(host=CLICKHOUSE_HOST)
            client.execute('DROP TABLE IF EXISTS docker.test;')
            client.execute('CREATE DATABASE IF NOT EXISTS docker;')
            client.execute('''
    CREATE TABLE IF NOT EXISTS docker.test (
    id UUID, user_id UUID, movie_id UUID, ts Int32, created Date)
    Engine=MergeTree PRIMARY KEY user_id;
    ''')
            self._pre_fill_db_mp(6, pre_filled_rec_count)

    @classmethod
    def _pre_fill_db_mp(cls, processes: int, rec_count: int) -> None:
        batch_size = rec_count // 50000
        with mp.Pool(processes) as pool:
            pool.map(cls._pre_fill_db, [50000 for _ in range(batch_size)])

    @staticmethod
    def _pre_fill_db(rec_count: int):
        client = Client(host=CLICKHOUSE_HOST)
        _data = [rec.dict() for rec in get_test_records(rec_count)]
        client.execute('INSERT INTO docker.test SETTINGS async_insert=1, wait_for_async_insert=1 VALUES', _data)

    def test_read(self, iter_count: int = 10) -> dict[str, any]:
        client = Client(host=CLICKHOUSE_HOST)
        t_sum = 0.

        for _ in range(iter_count):
            t_start = monotonic()
            client.execute(self.READ_QUERY)
            t_sum += monotonic() - t_start

        return {'test_read': {
            'operation': self.READ_QUERY,
            'iterations': iter_count,
            'avg_seconds': t_sum / iter_count
        }}

    def test_write(self, rec_count: int = 10000, iter_count: int = 10) -> dict[str, any]:
        client = Client(host=CLICKHOUSE_HOST)

        t_sum = 0.
        _data = [rec.dict() for rec in get_test_records(rec_count)]
        for _ in range(iter_count):
            t_start = monotonic()
            client.execute('INSERT INTO docker.test SETTINGS async_insert=1, wait_for_async_insert=1 VALUES', _data)
            t_sum += monotonic() - t_start

        return {'test_write': {
            'rec_count': rec_count,
            'iterations': iter_count,
            'avg_seconds': t_sum / iter_count
        }}


__all__ = ['ClickhouseTests']
