from pydantic import BaseModel
from datetime import datetime


class Rating(BaseModel):
    likes_count: int
    dislikes_count: int


class Review(BaseModel):
    text: str
    date: datetime
    author: str
    author_rating: int
    rating: Rating | None
