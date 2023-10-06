from uuid import UUID

from pydantic import BaseModel


class Mailing(BaseModel):
    mailing_id: UUID
    template_id: UUID
    template_params: UUID
    recipients_list: list[UUID]
