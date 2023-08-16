from datetime import datetime

from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


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


class IndexItemList(BaseModel):
    count: int
    total_pages: int
    prev: int | None
    next: int | None
    results: list = list[HistorySchema]
