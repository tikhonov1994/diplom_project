from aiohttp import ClientSession
import pytest
from http import HTTPStatus

ENDPOINT = '/auth/api/v1/roles/'
pytestmark = pytest.mark.asyncio


async def test_add_role(http_auth_client) -> None:
    http_auth_client: ClientSession
    new_role_name = 'new_role'

    async with http_auth_client.get(ENDPOINT) as response:
        assert response.status == HTTPStatus.OK
        data = await response.json()
        for item in data:
            assert item['name'] != new_role_name

    async with http_auth_client.post(ENDPOINT, json={'name': new_role_name}) as response:
        assert response.status == HTTPStatus.OK

    async with http_auth_client.get(ENDPOINT) as response:
        assert response.status == HTTPStatus.OK
        data = await response.json()
        names = [item['name'] for item in data]
        assert new_role_name in names
