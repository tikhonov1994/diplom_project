from uuid import UUID

from httpx import HTTPStatusError

from utils.backoff import async_backoff
from core.config import app_config as cfg
from schemas.notification import MailTemplateSchema
from adapters.adapter_base import ServiceAdapterBase


class AdminServiceAdapter(ServiceAdapterBase):
    def __init__(self):
        super().__init__(base_url=f'http://{cfg.admin.host}:{cfg.admin.port}/admin/templates/v1')

    @async_backoff(exceptions=HTTPStatusError)
    async def get_mail_template(self, template_id: UUID) -> MailTemplateSchema:
        response = await self._client.post(f'/{template_id}')
        response.raise_for_status()
        return MailTemplateSchema.model_validate(response.json())
