# flake8: noqa F541

import multiprocessing as mp
import psycopg2
from time import monotonic
from uuid import uuid4
from psycopg2.extras import RealDictCursor
from test_base import TestBase
from data_generator import gen_reviews, gen_likes, get_random_user

_POSTGRES_HOST = '127.0.0.1'
_POSTGRES_PORT = 5432
_POSTGRES_USER = 'app'
_POSTGRES_PASSWORD = 'hackme'
_POSTGRES_DATABASE = 'movies_database'

conn_info = {
    'dbname': _POSTGRES_DATABASE,
    'user': _POSTGRES_USER,
    'password': _POSTGRES_PASSWORD,
    'host': _POSTGRES_HOST,
    'port': _POSTGRES_PORT
}

pg_conn = psycopg2.connect(**conn_info)
psycopg2.extras.register_uuid()

# noinspection SqlNoDataSourceInspection
REVIEWS_CLEANUP_QUERY = f'DROP TABLE IF EXISTS reviews;'
LIKES_CLEANUP_QUERY = f'DROP TABLE IF EXISTS likes;'

CLEANUP_QUERIES = [
    REVIEWS_CLEANUP_QUERY,
    LIKES_CLEANUP_QUERY
]

REVIEWS_DDL_QUERY = 'CREATE TABLE IF NOT EXISTS reviews (review_id UUID PRIMARY KEY, film_id UUID, user_id UUID, ' \
                    'text TEXT, added DATE, author_rating INTEGER);'
LIKES_DDL_QUERY = 'CREATE TABLE IF NOT EXISTS likes (entity_id UUID, user_id UUID, value SMALLINT, added DATE);'
LIKES_INDEX_QUERY = 'CREATE INDEX IF NOT EXISTS user_entity_idx ON likes(user_id, entity_id);'
SETUP_QUERIES = [
    REVIEWS_DDL_QUERY,
    LIKES_DDL_QUERY,
    LIKES_INDEX_QUERY,
]


class PostgresTests(TestBase):
    READ_QUERY = f'SELECT * FROM reviews LEFT JOIN likes ON reviews.review_id = likes.entity_id where reviews.user_id = %s;'
    AVG_QUERY = f'SELECT AVG(value) FROM likes WHERE entity_id = %s GROUP BY entity_id;'
    COUNT_LIKES_QUERY = f'SELECT COUNT(*) FROM likes where likes.user_id = %s and value = 10;'

    def __init__(self, pre_filled_rec_count: int, cold_init: bool = True):
        if cold_init:
            with pg_conn as conn:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                try:
                    for query in CLEANUP_QUERIES:
                        cur.execute(query)
                    pass
                finally:
                    for query in SETUP_QUERIES:
                        cur.execute(query)
                    cur.close()
                    conn.commit()
            self._pre_fill_db_mp(6, pre_filled_rec_count)

    @classmethod
    def _pre_fill_db_mp(cls, processes: int, rec_count: int) -> None:
        batch_size = rec_count // 50000
        with mp.Pool(processes) as pool:
            pool.map(cls._pre_fill_reviews_db, [50000 for _ in range(batch_size)])
            pool.map(cls._pre_fill_likes_db, [50000 for _ in range(batch_size)])

    @staticmethod
    def _pre_fill_reviews_db(rec_count: int) -> None:
        with pg_conn as conn:
            cur = conn.cursor()
            records = [rec.dict() for rec in gen_reviews(rec_count)]
            records_list_template = ','.join(['%s'] * len(records))
            insert_query = 'INSERT INTO reviews (review_id, film_id, text, added, user_id, author_rating) values {}'.format(records_list_template)
            batch = [tuple(rec.values()) for rec in records]
            cur.execute(insert_query, batch)

            cur.close()
            conn.commit()

    @staticmethod
    def _pre_fill_likes_db(rec_count: int) -> None:
        with pg_conn as conn:
            cur = conn.cursor()

            records = [rec.dict() for rec in gen_likes(rec_count)]
            records_list_template = ','.join(['%s'] * len(records))
            query = 'INSERT INTO likes (entity_id, user_id, value, added) values {}'.format(records_list_template)
            batch = [tuple(rec.values()) for rec in records]
            cur.execute(query, batch)

            cur.close()
            conn.commit()

    def test_read(self, n: int = 10) -> dict[str, any]:
        with pg_conn as conn:
            cur = conn.cursor()

            t_sum = 0.
            for _ in range(n):
                user_id = get_random_user()['id']
                t_start = monotonic()
                cur.execute(self.READ_QUERY, [user_id])
                cur.fetchall()
                t_sum += monotonic() - t_start

            cur.close()
            conn.commit()

            return {'test_read': {
                'operation': self.READ_QUERY,
                'iterations': n,
                'avg_seconds': t_sum / n
            }}

    def test_read_avg_likes(self, n: int = 10) -> dict[str, any]:
        with pg_conn as conn:
            cur = conn.cursor()

            t_sum = 0.
            for _ in range(n):
                t_start = monotonic()
                cur.execute(self.AVG_QUERY, [uuid4()])
                cur.fetchall()
                t_sum += monotonic() - t_start

            cur.close()
            conn.commit()

            return {'test_read_avg': {
                'operation': self.AVG_QUERY,
                'iterations': n,
                'avg_seconds': t_sum / n
            }}

    def test_count_likes(self, n: int = 10) -> dict[str, any]:
        with pg_conn as conn:
            cur = conn.cursor()

            t_sum = 0.
            for _ in range(n):
                user_id = get_random_user()['id']
                t_start = monotonic()
                cur.execute(self.COUNT_LIKES_QUERY, [user_id])
                cur.fetchall()
                t_sum += monotonic() - t_start

            cur.close()
            conn.commit()

            return {'test_count_likes': {
                'operation': self.COUNT_LIKES_QUERY,
                'iterations': n,
                'avg_seconds': t_sum / n
            }}

    def test_write(self, rec_count: int = 10000, iter_count: int = 10) -> dict[str, any]:
        with pg_conn as conn:
            cur = conn.cursor()

            t_sum = 0.
            for _ in range(iter_count):
                test_records = [rec.dict() for rec in gen_reviews(rec_count)]
                records_list_template = ','.join(['%s'] * len(test_records))
                query = 'INSERT INTO reviews (review_id, film_id, text, added, user_id, author_rating) values {}'\
                    .format(records_list_template)
                batch = [tuple(rec.values()) for rec in test_records]

                t_start = monotonic()
                cur.execute(query, batch)
                t_sum += monotonic() - t_start

            cur.close()
            conn.commit()

            return {'test_write': {
                'rec_count': rec_count,
                'iterations': iter_count,
                'avg_seconds': t_sum / iter_count
            }}


__all__ = ['PostgresTests']
