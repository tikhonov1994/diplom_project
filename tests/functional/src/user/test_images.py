from http import HTTPStatus

import pytest
from aiohttp.client import ClientSession
from aiohttp import FormData
from functional.test_data.auth_data import test_auth_headers

ENDPOINT = '/user_api/api/v1/images/user-avatar'

pytestmark = pytest.mark.asyncio


async def test_add_avatar_auth(http_user_client: ClientSession) -> None:
    with open('./functional/test_data/test-image-good.jpg', 'rb') as f:
        data = FormData()
        data.add_field('image', f, content_type='image/jpg')
        async with http_user_client.post(ENDPOINT, data=data) as response:
            assert response.status == HTTPStatus.FORBIDDEN


async def test_add_safe_avatar(http_user_client: ClientSession,
                               http_minio_client: ClientSession) -> None:
    with open('./functional/test_data/test-image-good.jpg', 'rb') as f:
        data = FormData()
        data.add_field('image', f, content_type='image/jpg')
        async with http_user_client.post(ENDPOINT, data=data, headers=test_auth_headers) as response:
            # raise ValueError(await response.json())
            assert response.status == HTTPStatus.ACCEPTED
            ...
        # TODO: wait for some time (due to async processing), then check minio...


async def test_add_unsafe_avatar(http_user_client: ClientSession,
                                 http_minio_client: ClientSession) -> None:
    ...


async def test_add_invalid_avatar_type(http_user_client: ClientSession,
                                       http_minio_client: ClientSession) -> None:
    ...


async def test_change_avatar(http_user_client: ClientSession,
                             http_minio_client: ClientSession) -> None:
    ...
