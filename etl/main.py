import psycopg2
from psycopg2.extras import DictCursor
from time import sleep
from dotenv import load_dotenv
from contextlib import contextmanager
from elasticsearch import Elasticsearch
from etl_runner import ETL
from configs import app_config as config
from logger import logger
from sentry_sdk import capture_exception

load_dotenv()


@contextmanager
def get_pg_conn():
    conn = psycopg2.connect(**config.pg.dsl, cursor_factory=DictCursor)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_es_conn():
    conn = Elasticsearch(f"http://{config.elastic.host}:{config.elastic.port}")
    try:
        yield conn
    finally:
        conn.close()


if __name__ == '__main__':
    logger.info('ETL process started')
    with get_pg_conn() as pg_conn, get_es_conn() as es_conn:
        while True:
            try:
                ETL(es_conn, pg_conn, 'film_work', 'movies').run_movie_process()
                ETL(es_conn, pg_conn, 'person', 'persons').run_person_process()
                ETL(es_conn, pg_conn, 'genre', 'genres').run_genre_process()
                sleep(30)
            except Exception as e:
                capture_exception(e)
