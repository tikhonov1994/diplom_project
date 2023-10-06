from uuid import UUID

from core.config import app_config as cfg
from schemas.notification import MailTemplate
from adapters.adapter_base import ServiceAdapterBase


class NotificationServiceAdapter(ServiceAdapterBase):
    def __init__(self):
        super().__init__(base_url=f'http://{cfg.notification.host}:{cfg.notification.port}/auth/api/v1')

    async def get_mail_template(self, template_id: UUID) -> MailTemplate:
        response = await self._client.post(f'/template/{template_id}')
        response.raise_for_status()
        return MailTemplate.model_validate(response.json())
