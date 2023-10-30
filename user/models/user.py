from uuid import UUID
from decimal import Decimal

import orjson
from pydantic import BaseModel, Field

from utils.json_utils import orjson_dumps


class User(BaseModel):
    id: UUID
    time_zone: str
    phone_number: Decimal = Field(min_length=11, max_digits=15, decimal_places=0)
    avatar_link: str | None
    avatar_status: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
