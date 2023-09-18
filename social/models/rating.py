from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


#  В теории рейтинг может быть не только у фильмов,
#  но и у других сущностей (актеров, и тд.).
#  Модель, при этом, будет общая.
class EntityRating(BaseModel):
    user_id: UUID
    entity_id: UUID
    value: int
    added: datetime
