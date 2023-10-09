from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel


class NotificationTypes(Enum):
    DEFAULT = 'default'
    REGISTRATION = 'registration'


# todo мб позже разделить схему на create и тд, пока так
class NotificationRequestSchema(BaseModel):
    # recipients_list: set[UUID]
    recipients_list: list[UUID]
    subject: str
    template_id: UUID
    template_params: dict


class RegistrationNotificationSchema(BaseModel):
    id: UUID
    receiver_id: UUID
    type: NotificationTypes


class NotificationMessageSchema(BaseModel):
    notification_id: str
    subject: str
    recipients_list: list[str]
    template_id: str
    template_params: dict
