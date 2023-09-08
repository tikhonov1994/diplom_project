from uuid import UUID

from pydantic import BaseModel


class ViewsMessage(BaseModel):
    timestamp: int
    user_id: UUID
    movie_id: UUID
    created: int
