from uuid import UUID

from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: UUID = Field(alias='sub')
    email: str
    role: str
    user_agent: str
