from hashlib import md5
from http import HTTPStatus
from io import BytesIO
import json
from typing import Annotated

from fastapi import Depends, HTTPException
from minio import Minio

from adapters.file_storage.base import BaseSyncFileStorage
from core.config import app_config

_BUCKET_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
            "Resource": f"arn:aws:s3:::{app_config.api.minio_image_bucket}",
        },
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{app_config.api.minio_image_bucket}/*",
        },
    ],
}


class MinioFileStorage(BaseSyncFileStorage):
    def __init__(self) -> None:
        self.client = Minio(app_config.minio.endpoint,
                            app_config.minio.root_user,
                            app_config.minio.root_password,
                            secure=False)
        self._check_buckets()

    def save(self, origin_file_name: str, image_bytes: bytes, content_type: str) -> str:
        write_result = self.client.put_object(bucket_name=app_config.api.minio_image_bucket,
                                              object_name=MinioFileStorage.get_filename(image_bytes,
                                                                                        origin_file_name),
                                              data=BytesIO(image_bytes),
                                              length=len(image_bytes),
                                              content_type=content_type)
        return f'{write_result.bucket_name}/{write_result.object_name}'

    def load(self, object_name: str) -> bytes:
        with self.client.get_object(app_config.api.minio_image_bucket, object_name) as response:
            if response.status != HTTPStatus.OK:
                raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                                    detail='File service temporarily unavailable.')
            return response.data

    def delete(self, object_name: str) -> None:
        self.client.remove_object(app_config.api.minio_image_bucket, object_name)

    def _check_buckets(self):
        if not self.client.bucket_exists(app_config.api.minio_image_bucket):
            self.client.make_bucket(app_config.api.minio_image_bucket)
            self.client.set_bucket_policy(app_config.api.minio_image_bucket,
                                          json.dumps(_BUCKET_POLICY))

    @classmethod
    def get_filename(cls, payload: bytes, name: str) -> str:
        return f'{md5(payload).hexdigest()}{cls._get_ext(name)}'

    @staticmethod
    def _get_ext(filename: str) -> str:
        chunks = filename.split('.')
        return '.' + chunks[-1] if len(chunks) > 1 else ""


MinioFileStorageDep = Annotated[MinioFileStorage, Depends()]
