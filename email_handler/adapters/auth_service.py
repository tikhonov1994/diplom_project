from uuid import UUID

from httpx import HTTPStatusError

from utils.backoff import async_backoff
from core.config import app_config as cfg
from schemas.auth import UserInfoSchema
from adapters.adapter_base import ServiceAdapterBase


class AuthServiceAdapter(ServiceAdapterBase):
    def __init__(self):
        super().__init__(base_url=f'http://{cfg.auth.host}:{cfg.auth.port}/auth/api/v1')

    @async_backoff(exceptions=HTTPStatusError)
    async def get_user_info(self, user_id: UUID) -> UserInfoSchema:
        response = await self._client.post(f'/info/{user_id}')
        response.raise_for_status()
        return UserInfoSchema.model_validate(response.json())
