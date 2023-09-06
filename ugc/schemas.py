import uuid

from pydantic import BaseModel


class UserTimecodeSchema(BaseModel):
    timestamp: int
    user_id: uuid.UUID
    movie_id: uuid.UUID
