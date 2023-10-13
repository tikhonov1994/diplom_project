from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr


class CreateMailingRequestSchema(BaseModel):
    recipients_list: list[UUID]
    subject: str
    template_id: UUID
    template_params: dict


class MailingMessageSchema(BaseModel):
    mailing_id: str
    subject: str
    recipients_list: list[str]
    template_id: str
    template_params: dict


class MailingStatusEnum(str, Enum):
    created = 'CREATED'
    in_progress = 'IN_PROGRESS'
    done = 'DONE'
    failed = 'FAILED'


class UpdateMailingStatusRequestSchema(BaseModel):
    mailing_id: str
    status: MailingStatusEnum


class UserRegisterMailingSchema(BaseModel):
    user_id: UUID
    email: EmailStr
