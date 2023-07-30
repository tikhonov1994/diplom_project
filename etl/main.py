import psycopg2
import logging
from psycopg2.extras import DictCursor
from time import sleep
from dotenv import load_dotenv
from contextlib import contextmanager
from elasticsearch import Elasticsearch
from etl_runner import ETL
from configs import app_config as config

load_dotenv()
logging.basicConfig(filename=config.log_filename, level=config.logging_level,
                    format='%(asctime)s  %(message)s')
logger = logging.getLogger(__name__)


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
            ETL(es_conn, pg_conn, 'film_work', 'movies').run_movie_process()
            ETL(es_conn, pg_conn, 'person', 'persons').run_person_process()
            ETL(es_conn, pg_conn, 'genre', 'genres').run_genre_process()
            sleep(30)
