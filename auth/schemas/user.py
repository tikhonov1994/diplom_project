from uuid import UUID

from pydantic import BaseModel

from schemas.role import UserRoleSchema


class UserInfoSchema(BaseModel):
    id: UUID
    email: str
    role: UserRoleSchema
