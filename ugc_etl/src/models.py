from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ViewsMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    ts: int
    user_id: UUID
    movie_id: UUID
    created: int
