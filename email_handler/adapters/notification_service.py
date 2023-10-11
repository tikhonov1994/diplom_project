from uuid import UUID

from httpx import HTTPStatusError

from utils.backoff import async_backoff
from core.config import app_config as cfg
from schemas.mailing import MailingStatusSchema, MailingStatusEnum
from adapters.adapter_base import ServiceAdapterBase


class NotificationServiceAdapter(ServiceAdapterBase):
    def __init__(self):
        # TODO: check the route
        super().__init__(base_url=f'http://{cfg.notification.host}:{cfg.notification.port}/admin/api/v1')

    @async_backoff(exceptions=HTTPStatusError)
    async def post_mailing_status(self,
                                  request_id: UUID,
                                  mailing_id: UUID,
                                  mailing_status: MailingStatusEnum) -> None:
        headers = {'x-request-id': str(request_id)}
        body = MailingStatusSchema(mailing_id=mailing_id, mailing_status=mailing_status).model_dump()
        response = await self._client.post(f'/mailing/{mailing_id}/status', headers=headers, data=body)
        response.raise_for_status()
