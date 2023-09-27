from datetime import datetime
from random import choice, randint
from typing import Generator
from uuid import UUID, uuid4

from faker import Faker
from pydantic import BaseModel

faker = Faker()


class TestRecord(BaseModel):
    id: UUID
    user_id: UUID
    movie_id: UUID
    ts: int
    created: datetime


class Rating(BaseModel):
    likes_count: int
    dislikes_count: int


class Review(BaseModel):
    film_id: UUID
    text: str
    date: datetime
    author: str
    author_rating: int
    rating: Rating


def _get_rating() -> Rating:
    return Rating(
        likes_count=randint(0, 10000),
        dislikes_count=randint(0, 10000),
    )

def get_test_reviews(n: int) -> Generator[TestRecord, None, None]:

    user_ids = [uuid4() for _ in range(n // 10)] or [uuid4(), ]
    movie_ids = [uuid4() for _ in range(n // 50)] or [uuid4(), ]

    for _ in range(n):
        yield Review(
            film_id=choice(movie_ids),
            text=faker.text(max_nb_chars=1000),
            date=datetime.now(),
            author=faker.name(),
            author_rating=randint(0, 100),
            rating=_get_rating(),
        )
