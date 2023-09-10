import uuid

from pydantic import BaseModel


class UserTimecodeSchema(BaseModel):
    timestamp: int
    movie_id: uuid.UUID
