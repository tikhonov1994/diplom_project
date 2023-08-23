from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr
from schemas.base import IndexItemList


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


class HistoryListSchema(IndexItemList):
    results = list[HistorySchema]


class LoginResponseSchema(TokensSchema):
    user_id: UUID
    email: EmailStr
    role: str
