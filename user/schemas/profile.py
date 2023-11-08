from enum import Enum

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserProfileSchema(BaseModel):
    name: str
    surname: str
    country: str
    time_zone: str
    phone_number: PhoneNumber


class AvatarStatusesSchema(str, Enum):
    WITHOUT = 'WITHOUT'
    ON_INSPECTION = 'ON_INSPECTION'
    ACCEPTED = 'ACCEPTED'
    NON_ACCEPTED = 'NON_ACCEPTED'
