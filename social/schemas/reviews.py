from pydantic import BaseModel
from uuid import UUID


class ReviewSchema(BaseModel):
    film_id: UUID
    text: str
    author_rating: int
