import time
from http import HTTPStatus
import pytest
from aiohttp import ClientSession
from functional.test_data.auth_data import test_auth_headers
import uuid

VIEWS_ENDPOINT = '/ugc_api/api/v1/views/'

pytestmark = pytest.mark.asyncio


async def test_views(http_ugc_client: ClientSession) -> None:
    async with http_ugc_client.post(VIEWS_ENDPOINT, json={'timestamp': time.time(), 'movie_id': str(uuid.uuid4())},
                                    headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK
