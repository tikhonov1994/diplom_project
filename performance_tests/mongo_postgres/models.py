from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Review(BaseModel):
    review_id: UUID
    film_id: UUID
    text: str
    added: datetime
    user_id: UUID
    author_rating: int


class Likes(BaseModel):
    entity_id: UUID
    user_id: UUID
    value: int
    added: datetime
