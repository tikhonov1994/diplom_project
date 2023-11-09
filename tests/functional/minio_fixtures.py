import pytest

from minio import Minio

from settings import test_settings


@pytest.fixture(scope='session', autouse=True)
def clean_minio() -> None:
    client = Minio(f'{test_settings.minio_host}:{test_settings.minio_port}',
                   test_settings.minio_root_user,
                   test_settings.minio_root_password,
                   secure=False)
    images_to_delete = client.list_objects(test_settings.user_minio_image_bucket)
    for img in images_to_delete:
        client.remove_object(test_settings.user_minio_image_bucket, img.object_name)
