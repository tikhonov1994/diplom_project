# flake8: noqa F541

import multiprocessing as mp
from time import monotonic
from uuid import uuid4
from pymongo import MongoClient
from test_base import TestBase
from data_generator import gen_reviews, gen_likes, get_random_user

MONGO_HOST = 'mongos'
MONGO_PORT = 27017
MONGO_DB = 'social_db'


class MongoTests(TestBase):
    READ_QUERY = f'SELECT * FROM reviews where reviews.user_id = %s;'
    AVG_QUERY = f'SELECT AVG(value) FROM movieLikes WHERE entity_id = %s GROUP BY entity_id;'
    COUNT_LIKES_QUERY = f'SELECT COUNT(*) FROM likes where likes.user_id = %s and value = 10;'

    def __init__(self, pre_filled_rec_count: int, cold_init: bool = True):
        if cold_init:
            client = MongoClient(
                port=MONGO_PORT,
                uuidRepresentation='standard'
            )
            db = client[MONGO_DB]
            db.movieLikes.create_index([("user_id", 1)])
            db.movieLikes.create_index([("entity_id", 1)])
            db.reviews.create_index([("review_id", 1)])
            db.reviews.create_index([("user_id", 1)])
            self._pre_fill_db_mp(6, pre_filled_rec_count)

    @classmethod
    def _pre_fill_db_mp(cls, processes: int, rec_count: int) -> None:
        batch_size = rec_count // 50000
        with mp.Pool(processes) as pool:
            pool.map(cls._pre_fill_reviews, [50000 for _ in range(batch_size)])
            pool.map(cls._pre_fill_likes, [50000 for _ in range(batch_size)])

    @staticmethod
    def _pre_fill_reviews(rec_count: int):
        client = MongoClient(
            port=MONGO_PORT,
            uuidRepresentation='standard'
        )
        db = client[MONGO_DB]
        _data = [rec.dict() for rec in gen_reviews(rec_count)]
        db.reviews.insert_many(_data)

    @staticmethod
    def _pre_fill_likes(rec_count: int):
        client = MongoClient(
            port=MONGO_PORT,
            uuidRepresentation='standard'
        )
        db = client[MONGO_DB]
        _data = [rec.dict() for rec in gen_likes(rec_count)]
        db.movieLikes.insert_many(_data)

    def test_read(self, iter_count: int = 10) -> dict[str, any]:
        client = MongoClient(
            port=MONGO_PORT,
            uuidRepresentation='standard'
        )
        db = client[MONGO_DB]

        t_sum = 0.
        for _ in range(iter_count):
            user_id = get_random_user()['id']
            t_start = monotonic()
            db.movieLikes.find({
                "user_id": user_id
            })
            t_sum += monotonic() - t_start

        return {'test_read': {
            'operation': self.READ_QUERY,
            'iterations': iter_count,
            'avg_seconds': t_sum / iter_count
        }}

    def test_read_avg_likes(self, iter_count: int = 10) -> dict[str, any]:
        client = MongoClient(
            port=MONGO_PORT,
            uuidRepresentation='standard'
        )
        db = client[MONGO_DB]

        t_sum = 0.
        for _ in range(iter_count):
            t_start = monotonic()
            db.movieLikes.aggregate([
                {"$match": {"entity_id": uuid4()}},
                {'$group': {
                    '_id': "$entity_id",
                    'avg_rating': {
                        '$avg': "$value"
                    }}}
            ])
            t_sum += monotonic() - t_start

        return {'test_read_avg': {
            'operation': self.AVG_QUERY,
            'iterations': iter_count,
            'avg_seconds': t_sum / iter_count
        }}

    def test_count_likes(self, iter_count: int = 10) -> dict[str, any]:
        client = MongoClient(
            port=MONGO_PORT,
            uuidRepresentation='standard'
        )
        db = client[MONGO_DB]

        t_sum = 0.
        for _ in range(iter_count):
            user_id = get_random_user()['id']
            t_start = monotonic()
            db.movieLikes.count_documents({
                "user_id": user_id,
                "value": 10
            })
            t_sum += monotonic() - t_start

        return {'test_count_likes': {
            'operation': self.COUNT_LIKES_QUERY,
            'iterations': iter_count,
            'avg_seconds': t_sum / iter_count
        }}

    def test_write(self, rec_count: int = 10000, iter_count: int = 1) -> dict[str, any]:
        client = MongoClient(
            port=MONGO_PORT,
            uuidRepresentation='standard'
        )
        db = client[MONGO_DB]

        t_sum = 0.
        for _ in range(iter_count):
            _data = [rec.dict() for rec in gen_reviews(rec_count)]
            t_start = monotonic()
            db.movieLikes.insert_many(_data)
            t_sum += monotonic() - t_start

        return {'test_write': {
            'rec_count': rec_count,
            'iterations': iter_count,
            'avg_seconds': t_sum / iter_count
        }}


__all__ = ['MongoTests']
