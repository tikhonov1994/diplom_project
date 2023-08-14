from typing import Annotated, Optional

from fastapi import Depends
from redis.asyncio import Redis

redis: Optional[Redis] = None


async def get_redis() -> Redis:
    return redis


RedisDep = Annotated[Redis, Depends(get_redis)]
