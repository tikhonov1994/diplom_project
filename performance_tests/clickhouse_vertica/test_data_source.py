from datetime import datetime
from random import choice, randint
from typing import Generator
from uuid import UUID, uuid4

from pydantic import BaseModel


class TestRecord(BaseModel):
    id: UUID
    user_id: UUID
    movie_id: UUID
    ts: int
    created: datetime


def get_test_records(n: int) -> Generator[TestRecord, None, None]:

    user_ids = [uuid4() for _ in range(n // 10)] or [uuid4(), ]
    movie_ids = [uuid4() for _ in range(n // 50)] or [uuid4(), ]

    for _ in range(n):
        yield TestRecord(
            id=uuid4(),
            user_id=choice(user_ids),
            movie_id=choice(movie_ids),
            ts=randint(0, 3600),
            created=datetime.now()
        )
