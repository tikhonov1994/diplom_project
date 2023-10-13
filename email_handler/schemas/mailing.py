from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class MailingStatusEnum(str, Enum):
    created = 'CREATED'
    in_progress = 'IN_PROGRESS'
    done = 'DONE'
    failed = 'FAILED'


class MailingSchema(BaseModel):
    mailing_id: UUID
    template_id: UUID
    subject: str
    template_params: dict
    recipients_list: set[UUID]
    request_id: UUID | None = None
    retries_cnt: int = 0


class MailingStatusSchema(BaseModel):
    mailing_id: UUID
    mailing_status: MailingStatusEnum
    message: str | None = None
