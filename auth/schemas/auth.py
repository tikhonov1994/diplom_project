from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str
    password: str


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        orm_mode = True