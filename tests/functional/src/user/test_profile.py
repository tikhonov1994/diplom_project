from http import HTTPStatus
from asyncio import sleep
from hashlib import md5

import pytest
from aiohttp.client import ClientSession
from aiohttp import FormData

from functional.test_data.auth_data import test_auth_headers
from functional.test_data.user_data import test_user_profile_create_schema
from settings import test_settings as settings

BASE_ENDPOINT = '/user_api/api/v1/profile/'

pytestmark = pytest.mark.asyncio


async def test_add_profile_auth(http_user_client: ClientSession) -> None:
    async with http_user_client.post(f'{BASE_ENDPOINT}add', json=test_user_profile_create_schema) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_add_profile(http_user_client: ClientSession) -> None:
    async with http_user_client.post(f'{BASE_ENDPOINT}add', json=test_user_profile_create_schema) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_change_avatar(http_user_client: ClientSession,
                             http_minio_client: ClientSession) -> None:
    img1 = './functional/test_data/test-image-good.jpg'
    img2 = './functional/test_data/test-image-good-2.jpg'
    with open(img1, 'rb') as f:
        _bytes_1 = f.read()
    with open(img2, 'rb') as f:
        _bytes_2 = f.read()
    assert (await _file_exists(http_minio_client, _bytes_2, img2)) is False

    data1 = FormData()
    data1.add_field('image', _bytes_1, content_type='image/jpg', filename='image1.jpg')
    async with http_user_client.post(ENDPOINT, data=data1, headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.ACCEPTED
        await sleep(0.5)
        assert (await _file_exists(http_minio_client, _bytes_1, img1)) is True

    data2 = FormData()
    data2.add_field('image', _bytes_2, content_type='image/jpg', filename='image2.jpg')
    async with http_user_client.post(ENDPOINT, data=data2, headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.ACCEPTED
        await sleep(0.5)
        assert (await _file_exists(http_minio_client, _bytes_2, img1)) is True
        assert (await _file_exists(http_minio_client, _bytes_1, img1)) is False
