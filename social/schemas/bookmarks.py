from uuid import UUID

from pydantic import BaseModel


class BookmarkSchema(BaseModel):
    film_id: UUID
