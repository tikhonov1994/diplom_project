from pydantic import BaseModel


class Message(BaseModel):
    # todo decode fields
    timestamp: str
    user_id: str
    movie_id: str
