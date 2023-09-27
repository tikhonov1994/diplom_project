from typing import Annotated  # type: ignore[attr-defined]

from db.storage.rating import RatingStorage
from db.storage.review import ReviewStorage
from fastapi import Depends

ReviewStorageDep = Annotated[ReviewStorage, Depends()]
RatingStorageDep = Annotated[RatingStorage, Depends()]

__all__ = ['ReviewStorageDep',
           'RatingStorageDep']
