from typing import Annotated, Optional

from fastapi import Depends, Request
from redis.asyncio import Redis

redis: Optional[Redis] = None


async def get_redis() -> Redis:
    return redis


def request_key_builder(
        _,
        namespace: str = "",
        request: Request = None,
        *__,
        **___,
):
    return ":".join([
        namespace,
        request.method.lower(),
        request.url.path,
        repr(sorted(request.query_params.items()))
    ])


RedisDep = Annotated[Redis, Depends(get_redis)]
