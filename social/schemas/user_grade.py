from uuid import UUID

from pydantic import BaseModel


class UserSocialGradeResponse(BaseModel):
    user_id: UUID
    social_rating: float
