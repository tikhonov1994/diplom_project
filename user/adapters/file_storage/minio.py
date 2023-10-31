from hashlib import md5
from http import HTTPStatus
from io import BytesIO
import json
from typing import Annotated

from fastapi import Depends, HTTPException
from minio import Minio

from adapters.file_storage.base import BaseFileStorage
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


class MinioFileStorage(BaseFileStorage):
    def __init__(self) -> None:
        self.client = Minio(app_config.minio.endpoint,
                            app_config.minio.root_user,
                            app_config.minio.root_password,
                            secure=False)

    async def save(self, origin_file_name: str, image_bytes: bytes, content_type: str) -> str:
        write_result = self.client.put_object(bucket_name=app_config.api.minio_image_bucket,
                                              object_name=f'{md5(image_bytes).hexdigest()}'
                                                          f'{self._get_ext(origin_file_name)}',
                                              data=BytesIO(image_bytes),
                                              length=len(image_bytes),
                                              content_type=content_type)
        # TODO: Check This :>
        return write_result.object_name

    async def load(self, object_name: str) -> bytes:
        with self.client.get_object(app_config.api.minio_image_bucket, object_name) as response:
            if response.status != HTTPStatus.OK:
                raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                                    detail='File service temporarily unavailable.')
            return response.data

    async def _check_buckets(self):
        if not self.client.bucket_exists(app_config.api.minio_image_bucket):
            self.client.make_bucket(app_config.api.minio_image_bucket)
            self.client.set_bucket_policy(app_config.api.minio_image_bucket,
                                          json.dumps(_BUCKET_POLICY))

    @staticmethod
    def _get_ext(filename: str) -> str:
        chunks = filename.split('.')
        return '.' + chunks[-1] if len(chunks) > 1 else ""


MinioFileStorageDep = Annotated[MinioFileStorage, Depends()]
