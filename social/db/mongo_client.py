from typing import Annotated

from core.config import app_config
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

_client = AsyncIOMotorClient(
    app_config.mongo.host,
    app_config.mongo.port,
    uuidRepresentation='standard'
)


def get_mongo_client() -> AsyncIOMotorClient:  # type: ignore[valid-type]
    return _client


MongoClientDep = Annotated[AsyncIOMotorClient, Depends(get_mongo_client)]  # type: ignore[valid-type]

__all__ = ['MongoClientDep']
