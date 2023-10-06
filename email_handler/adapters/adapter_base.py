from httpx import AsyncClient


class ServiceAdapterBase:
    def __init__(self, base_url: str):
        self._client = AsyncClient(base_url=base_url, verify=False)

    def __del__(self):
        await self._client.aclose()


__all__ = ['ServiceAdapterBase']
