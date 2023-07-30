import uuid

import orjson
from pydantic import BaseModel

from utils.json_utils import orjson_dumps


class Base(BaseModel):
    id: uuid.UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class IndexItemList(BaseModel):
    count: int
    total_pages: int
    prev: int | None
    next: int | None
    results: list

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
