from typing import Annotated  # type: ignore[attr-defined]

from fastapi import Depends
from services.rating import MovieRatingService
from services.reviews import ReviewService
from services.bookmarks import BookmarksService
from services.user_grade import UserGradeService

ReviewServiceDep = Annotated[ReviewService, Depends()]
MovieRatingServiceDep = Annotated[MovieRatingService, Depends()]
BookmarkServiceDep = Annotated[BookmarksService, Depends()]
UserGradeServiceDep = Annotated[UserGradeService, Depends()]

__all__ = ['ReviewServiceDep',
           'MovieRatingServiceDep',
           'BookmarkServiceDep',
           'UserGradeServiceDep']
