from typing import Annotated
from db.storage.mongo import MongoStorage
from fastapi import Depends

MongoStrageDep = Annotated[MongoStorage, Depends()]

__all__ = ['MongoStrageDep']
