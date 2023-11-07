from enum import Enum

from pydantic import BaseModel, Field
from decimal import Decimal


class UserProfileSchema(BaseModel):
    name: str
    surname: str
    country: str
    time_zone: str
    phone_number: Decimal = Field(max_digits=15, decimal_places=0)


class AvatarStatusesSchema(str, Enum):
    WITHOUT = 'WITHOUT'
    ON_INSPECTION = 'ON_INSPECTION'
    ACCEPTED = 'ACCEPTED'
    NON_ACCEPTED = 'NON_ACCEPTED'


