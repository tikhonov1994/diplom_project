from datetime import datetime
from random import choice, randint
from typing import Generator
from uuid import uuid4
from faker import Faker
from models import Review, Likes

faker = Faker()


def _get_user() -> dict:
    return {'id': uuid4(), 'name': faker.name()}


USERS = [_get_user() for _ in range(1000)]
MOVIE_IDS = [uuid4() for _ in range(1000)]


def get_random_user() -> dict:
    return choice(USERS)


def gen_reviews(n: int) -> Generator[Review, None, None]:
    for _ in range(n):
        user = choice(USERS)
        yield Review(
            review_id=uuid4(),
            film_id=choice(MOVIE_IDS),
            text=faker.text(max_nb_chars=1000),
            added=datetime.now(),
            user_id=user['id'],
            author_rating=randint(0, 100),
        )


def gen_likes(n: int, film_id=None) -> Generator[Likes, None, None]:
    for _ in range(n):
        user = choice(USERS)
        yield Likes(
            entity_id=film_id or choice(MOVIE_IDS),
            user_id=user['id'],
            value=randint(0, 10),
            added=datetime.now(),
        )
