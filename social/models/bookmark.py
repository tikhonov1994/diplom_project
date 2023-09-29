from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Bookmark(BaseModel):
    bookmark_id: UUID
    film_id: UUID
    user_id: UUID
    added: datetime
