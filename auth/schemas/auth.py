from datetime import datetime

from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str
    password: str


class RefreshSchema(BaseModel):
    refresh_token: str

    class Config:
        orm_mode = True


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        orm_mode = True


class HistorySchema(BaseModel):
    session_started: datetime
    session_ended: datetime | None
    user_agent: str
