from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class NsfwPredictionClass(str, Enum):
    sexy = 'Sexy'
    porn = 'Porn'
    hentai = 'Hentai'
    drawing = 'Drawing'
    neutral = 'Neutral'


class UserImageSchema(BaseModel):
    user_id: UUID
    mime: str
    data: bytes
    name: str


class UploadedUserImageSchema(UserImageSchema):
    storage_url: str


class NsfwPrediction(BaseModel):
    class_name: NsfwPredictionClass = Field(alias='className')
    probability: float


class NsfwPredictionList(BaseModel):
    predictions: list[NsfwPrediction] = Field(alias='prediction')


