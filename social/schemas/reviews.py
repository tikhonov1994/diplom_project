from uuid import UUID

from pydantic import BaseModel


class ReviewSchema(BaseModel):
    film_id: UUID
    text: str
    author_rating: int
