from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel


class NotificationTypes(Enum):
    DEFAULT = 'default'


class NotificationSchema(BaseModel):
    id: UUID
    receiver_ids: List[UUID]
    type: NotificationTypes
    template_id: UUID
    template_params: dict[str, any]
