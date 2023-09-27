from typing import Annotated

from db.storage.rating import RatingStorage
from db.storage.review import ReviewStorage
from db.storage.bookmark import BookmarkStorage
from fastapi import Depends

ReviewStorageDep = Annotated[ReviewStorage, Depends()]
RatingStorageDep = Annotated[RatingStorage, Depends()]
BookmarkStorageDep = Annotated[BookmarkStorage, Depends()]

__all__ = ['ReviewStorageDep',
           'RatingStorageDep',
           'BookmarkStorageDep',]
