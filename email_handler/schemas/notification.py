from uuid import UUID

from pydantic import BaseModel


class MailTemplateSchema(BaseModel):
    id: UUID
    body: str
