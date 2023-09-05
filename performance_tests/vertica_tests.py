import multiprocessing as mp
from time import monotonic

from vertica_python import connect

from test_base import TestBase
from test_params import DATA_FILE, TEST_TABLE_NAME

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
CLEANUP_QUERY = f'DROP TABLE {TEST_TABLE_NAME};'
# noinspection SqlNoDataSourceInspection
DDL_QUERY = f'''
CREATE TABLE {TEST_TABLE_NAME} (
time INT, place VARCHAR, status VARCHAR, 
tsunami BOOLEAN, significance INT, data_type VARCHAR, 
magnitudo FLOAT, state VARCHAR, longitude FLOAT, 
latitude FLOAT, depth FLOAT, date DATE);
'''


class VerticaTests(TestBase):
    # noinspection SqlNoDataSourceInspection
    READ_QUERY = f'select distinct state from {TEST_TABLE_NAME} where longitude > latitude;'

    def __init__(self, cold_init: bool = True):
        if cold_init:
            with connect(**conn_info) as conn:
                cur = conn.cursor()
                try:
                    cur.execute(CLEANUP_QUERY)
                except:
                    pass
                try:
                    cur.execute(DDL_QUERY)
                    with open(DATA_FILE, 'rb') as fs:
                        cur.copy(f'COPY {TEST_TABLE_NAME} FROM STDIN DELIMITER \',\' ENCLOSED BY \'"\'',
                                 fs, buffer_size=_WRITE_BUFFER_SIZE)
                except:
                    pass

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

    def test_write(self, chunk_file: str, n: int = 10) -> dict[str, any]:
        with connect(**conn_info) as conn:
            cur = conn.cursor()

            t_sum = 0.
            with open(chunk_file, 'rb') as chunk_f:
                for _ in range(n):
                    t_start = monotonic()
                    cur.copy(f'COPY {TEST_TABLE_NAME} FROM STDIN DELIMITER \',\' ENCLOSED BY \'"\'',
                             chunk_f, buffer_size=_WRITE_BUFFER_SIZE)
                    t_sum += monotonic() - t_start

            return {'test_write': {
                'chunk_file': chunk_file,
                'iterations': n,
                'avg_seconds': t_sum / n
            }}


__all__ = ['VerticaTests']
