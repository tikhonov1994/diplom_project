from typing import Annotated

from core.config import app_config
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

_client = AsyncIOMotorClient(
    app_config.mongo.host,
    app_config.mongo.port,
    uuidRepresentation='standard'
)


def get_mongo_client() -> AsyncIOMotorClient:
    return _client


MongoClientDep = Annotated[AsyncIOMotorClient, Depends(get_mongo_client)]

__all__ = ['MongoClientDep']
