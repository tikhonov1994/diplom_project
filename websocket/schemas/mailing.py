from uuid import UUID

from pydantic import BaseModel


class MailingSchema(BaseModel):
    mailing_id: UUID
    template_id: UUID
    subject: str
    template_params: dict
    recipients_list: set[UUID]
    request_id: UUID
    retries_cnt: int = 0
