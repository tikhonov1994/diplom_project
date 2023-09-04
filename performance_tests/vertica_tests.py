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

    # def test_read_mp(self, cores: int = 4, n: int = 10) -> dict[str, any]:
    #     with mp.Pool(cores) as pool:
    #         results = pool.map(self.test_read, [n for _ in range(cores)])
    #         avg_seconds = sum([test['test_read']['avg_seconds'] for test in results]) / len(results)
    #         return {'test_read_mp': {
    #             'operation': READ_QUERY,
    #             'cores': cores,
    #             'iterations': n,
    #             'avg_seconds': avg_seconds
    #         }}
    #
    # def test_write_mp(self, chunk_file: str, cores: int = 4, n: int = 4) -> dict[str, any]:
    #     with mp.Pool(cores) as pool:
    #         results = pool.starmap(self.test_write, [(chunk_file, n) for _ in range(cores)])
    #         avg_seconds = sum([test['test_write']['avg_seconds'] for test in results]) / len(results)
    #         return {'test_write_mp': {
    #             'chunk_file': chunk_file,
    #             'cores': cores,
    #             'iterations': n,
    #             'avg_seconds': avg_seconds
    #         }}
    #
    # def test_mixed_mp(self, chunk_file: str, cores: int = 4, n: int = 10) -> dict[str, any]:
    #     with mp.Pool(cores) as pool:
    #         args = []
    #         for c_idx in range(cores):
    #             args.append(('read' if c_idx % 2 else 'write', chunk_file, n))
    #         results = pool.starmap(self._work, args)
    #
    #         _r_cnt = _w_cnt = 0
    #         avg_read_seconds = avg_write_seconds = 0.
    #         for res in results:
    #             if read_res := res.get('test_read'):
    #                 _r_cnt += 1
    #                 avg_read_seconds += read_res.get('avg_seconds')
    #             elif write_res := res.get('test_write'):
    #                 _w_cnt += 1
    #                 avg_write_seconds += write_res.get('avg_seconds')
    #         avg_read_seconds /= _r_cnt
    #         avg_write_seconds /= _w_cnt
    #
    #         return {'test_mixed_mp': {
    #             'read_operation': self.READ_QUERY,
    #             'write_chunk_file': chunk_file,
    #             'cores': cores,
    #             'iterations': n,
    #             'avg_read_seconds': avg_read_seconds,
    #             'avg_write_seconds': avg_write_seconds
    #         }}


__all__ = ['VerticaTests']
