from time import monotonic
import multiprocessing as mp

from vertica_python import connect

from test_base import TestBase
from test_data_source import get_test_records

_VERTICA_HOST = 'localhost'
_VERTICA_PORT = 5433
_VERTICA_USER = 'dbadmin'
_VERTICA_PASSWORD = ''
_VERTICA_DATABASE = 'docker'

_WRITE_BUFFER_SIZE = 65536

conn_info = {
    'host': _VERTICA_HOST,
    'port': _VERTICA_PORT,
    'user': _VERTICA_USER,
    'password': _VERTICA_PASSWORD,
    'database': _VERTICA_DATABASE,

    'session_label': 'some_label',
    'unicode_error': 'strict',
    'ssl': False,
    'autocommit': True,
    'use_prepared_statements': False,
    'connection_timeout': 5
}

# noinspection SqlNoDataSourceInspection
CLEANUP_QUERY = 'DROP TABLE test;'
# noinspection SqlNoDataSourceInspection
DDL_QUERY = 'CREATE TABLE test (id UUID, user_id UUID, movie_id UUID, ts INT, created DATE);'


class VerticaTests(TestBase):
    # noinspection SqlNoDataSourceInspection
    READ_QUERY = 'select distinct user_id from test where ts > 2400;'

    def __init__(self, pre_filled_rec_count: int, cold_init: bool = True):
        if cold_init:
            with connect(**conn_info) as conn:
                cur = conn.cursor()
                try:
                    cur.execute(CLEANUP_QUERY)
                finally:
                    cur.execute(DDL_QUERY)
                    self._pre_fill_db_mp(6, pre_filled_rec_count)

    @classmethod
    def _pre_fill_db_mp(cls, processes: int, rec_count: int) -> None:
        batch_size = rec_count // 50000
        with mp.Pool(processes) as pool:
            pool.map(cls._pre_fill_db, [50000 for _ in range(batch_size)])

    @staticmethod
    def _pre_fill_db(rec_count: int) -> None:
        test_records = [rec.dict() for rec in get_test_records(rec_count)]
        with connect(**conn_info) as conn:
            cur = conn.cursor()
            cur.executemany('''INSERT INTO test (id, user_id, movie_id, ts, created) 
                                VALUES (:id, :user_id, :movie_id, :ts, :created);''',
                            test_records)

    def test_read(self, n: int = 10) -> dict[str, any]:
        with connect(**conn_info) as conn:
            cur = conn.cursor()

            t_sum = 0.
            for _ in range(n):
                t_start = monotonic()
                cur.execute(self.READ_QUERY).fetchall()
                t_sum += monotonic() - t_start

            return {'test_read': {
                'operation': self.READ_QUERY,
                'iterations': n,
                'avg_seconds': t_sum / n
            }}

    def test_write(self, rec_count: int = 10000, iter_count: int = 10) -> dict[str, any]:
        with connect(**conn_info) as conn:
            cur = conn.cursor()

            t_sum = 0.
            test_records = [rec.dict() for rec in get_test_records(rec_count)]
            for _ in range(iter_count):
                t_start = monotonic()
                cur.executemany('''INSERT INTO test (id, user_id, movie_id, ts, created) 
                                    VALUES (:id, :user_id, :movie_id, :ts, :created);''',
                                test_records)
                t_sum += monotonic() - t_start

            return {'test_write': {
                'rec_count': rec_count,
                'iterations': iter_count,
                'avg_seconds': t_sum / iter_count
            }}


__all__ = ['VerticaTests']
