from csv import DictReader
from datetime import datetime
import multiprocessing as mp
from time import monotonic

from clickhouse_driver import Client

from test_base import TestBase
from test_params import DATA_FILE, TEST_TABLE_NAME

CLICKHOUSE_HOST = 'localhost'


def _load_csv(file: str) -> list[dict]:
    converters = {
        'time': int,
        'tsunami': bool,
        'significance': int,
        'magnitudo': bool,
        'longitude': float,
        'latitude': float,
        'depth': float,
        'date': datetime.fromisoformat
    }

    data_items = []

    with open(file, 'r', encoding='utf8') as f:
        reader = DictReader(f)
        for line in reader:
            data_items.append({k: (converters[k](v) if k in converters else v) for k, v in line.items()})

    return data_items


# noinspection SqlNoDataSourceInspection
class ClickhouseTests(TestBase):
    READ_QUERY = f'select distinct state from docker.{TEST_TABLE_NAME} where longitude > latitude;'

    def __init__(self, cold_init: bool = True):
        if cold_init:
            client = Client(host=CLICKHOUSE_HOST)
            client.execute(f'DROP TABLE IF EXISTS docker.{TEST_TABLE_NAME};')
            client.execute('CREATE DATABASE IF NOT EXISTS docker ON CLUSTER company_cluster;')
            client.execute(f'''
    CREATE TABLE IF NOT EXISTS docker.{TEST_TABLE_NAME} ON CLUSTER company_cluster (
    time Int64, place String, status String, 
    tsunami Boolean, significance Int32, data_type String, 
    magnitudo Float32, state String, longitude Float32, 
    latitude Float32, depth Float32, date Date)
    Engine=MergeTree PRIMARY KEY latitude;
    ''')
            client.execute(f'INSERT INTO docker.{TEST_TABLE_NAME} VALUES ', _load_csv(DATA_FILE))

    def test_read(self, n: int = 10) -> dict[str, any]:
        client = Client(host=CLICKHOUSE_HOST)
        t_sum = 0.

        for _ in range(n):
            t_start = monotonic()
            client.execute(self.READ_QUERY)
            t_sum += monotonic() - t_start

        return {'test_read': {
            'operation': self.READ_QUERY,
            'iterations': n,
            'avg_seconds': t_sum / n
        }}

    def test_write(self, chunk_file: str, n: int = 10) -> dict[str, any]:
        client = Client(host=CLICKHOUSE_HOST)

        t_sum = 0.
        _data = _load_csv(chunk_file)
        for _ in range(n):
            t_start = monotonic()
            client.execute(f'INSERT INTO docker.{TEST_TABLE_NAME} VALUES', _data)
            t_sum += monotonic() - t_start

        return {'test_write': {
            'chunk_file': chunk_file,
            'iterations': n,
            'avg_seconds': t_sum / n
        }}


__all__ = ['ClickhouseTests']
