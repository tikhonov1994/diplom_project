from uuid import UUID

from pydantic import BaseModel


class MailingSchema(BaseModel):
    mailing_id: UUID
    subject: str
    body: str
    recipients_list: set[UUID]
    request_id: UUID | None = None
    retries_cnt: int = 0


class WebsocketMessageSchema(BaseModel):
    subject: str
    body: str
    request_id: UUID | None = None
