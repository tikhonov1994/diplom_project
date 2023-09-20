from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Rating(BaseModel):
    likes_count: int
    dislikes_count: int


class Review(BaseModel):
    film_id: UUID
    text: str
    date: datetime
    author: str
    author_rating: int
    rating: Rating | None
