from httpx import AsyncClient


class ServiceAdapterBase:
    def __init__(self, base_url: str):
        self._client = AsyncClient(base_url=base_url, verify=False)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self._client.aclose()


__all__ = ['ServiceAdapterBase']
