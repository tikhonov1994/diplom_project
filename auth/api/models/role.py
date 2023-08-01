from uuid import UUID

from pydantic import BaseModel


class UserRoleSchema(BaseModel):
    id: UUID
    name: str

    class Config:
        from_orm = True
