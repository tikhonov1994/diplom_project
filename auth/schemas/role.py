from uuid import UUID

from pydantic import BaseModel


class PatchUserRoleSchema(BaseModel):
    role_id: UUID


class AddUserRoleSchema(BaseModel):
    name: str


class UserRoleSchema(AddUserRoleSchema):
    id: UUID

    class Config:
        orm_mode = True
