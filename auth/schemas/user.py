from uuid import UUID

from pydantic import BaseModel, EmailStr
from schemas.role import UserRoleSchema


class UserInfoSchema(BaseModel):
    id: UUID
    email: str
    role: UserRoleSchema

    class Config:
        orm_mode = True


class UserSendEmailPayloadSchema(BaseModel):
    user_id: UUID
    email: EmailStr


class PatchUserInfoSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
