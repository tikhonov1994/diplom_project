from uuid import UUID

from pydantic import BaseModel


class MailTemplate(BaseModel):
    id: UUID
    body: str
