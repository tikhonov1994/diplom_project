from http import HTTPStatus
from asyncio import sleep
from hashlib import md5

import pytest
from aiohttp.client import ClientSession
from aiohttp import FormData

from functional.test_data.auth_data import test_auth_headers
from settings import test_settings as settings

ENDPOINT = '/user_api/api/v1/images/user-avatar'

pytestmark = pytest.mark.asyncio


def _get_ext(filename: str) -> str:
    chunks = filename.split('.')
    return '.' + chunks[-1] if len(chunks) > 1 else ""


def _get_filename(payload: bytes, name: str) -> str:
    return f'{md5(payload).hexdigest()}{_get_ext(name)}'


async def _file_exists(client: ClientSession, file_bytes: bytes, file_name: str) -> bool:
    bucket_file_name = _get_filename(file_bytes, file_name)
    async with client.get(f'/{settings.user_minio_image_bucket}/{bucket_file_name}') as response:
        if response.status == HTTPStatus.OK:
            return True
        elif response.status == HTTPStatus.NOT_FOUND:
            return False
    response.raise_for_status()


async def test_add_avatar_auth(http_user_client: ClientSession) -> None:
    with open('./functional/test_data/test-image-good.jpg', 'rb') as f:
        data = FormData()
        data.add_field('image', f, content_type='image/jpg')
        async with http_user_client.post(ENDPOINT, data=data) as response:
            assert response.status == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    'image_path, content_type, status_to_check, should_be_uploaded',
    [('./functional/test_data/test-image-good.jpg', 'image/jpg', HTTPStatus.ACCEPTED, True),
     ('./functional/test_data/test-image-bad.png', 'image/png', HTTPStatus.ACCEPTED, False),
     ('./functional/test_data/test-not-image.txt', 'text/plain', HTTPStatus.UNSUPPORTED_MEDIA_TYPE, False)]
)
async def test_add_avatar(http_user_client: ClientSession,
                          http_minio_client: ClientSession,
                          image_path: str,
                          content_type: str,
                          status_to_check: int,
                          should_be_uploaded: bool) -> None:
    with open(image_path, 'rb') as f:
        data = FormData()
        _bytes = f.read()
        data.add_field('image', _bytes, content_type=content_type, filename='image.jpg')
        async with http_user_client.post(ENDPOINT, data=data, headers=test_auth_headers) as response:
            assert response.status == status_to_check
            await sleep(0.5)
        assert (await _file_exists(http_minio_client, _bytes, image_path)) is should_be_uploaded


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
