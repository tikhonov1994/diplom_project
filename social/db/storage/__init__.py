from typing import Annotated
from db.storage.review import ReviewStorage
from db.storage.rating import RatingStorage
from fastapi import Depends

ReviewStorageDep = Annotated[ReviewStorage, Depends()]
RatingStorageDep = Annotated[RatingStorage, Depends()]

__all__ = ['ReviewStorageDep',
           'RatingStorageDep']
