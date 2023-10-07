from uuid import UUID

from pydantic import BaseModel


class UserRoleSchema(BaseModel):
    name: str
    id: UUID


class UserInfoSchema(BaseModel):
    id: UUID
    email: str
    role: UserRoleSchema

    @property
    def template_params(self) -> dict[str, any]:
        return {}
