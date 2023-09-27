from typing import Annotated

from fastapi import Depends
from services.rating import MovieRatingService
from services.reviews import ReviewService

ReviewServiceDep = Annotated[ReviewService, Depends()]
MovieRatingServiceDep = Annotated[MovieRatingService, Depends()]

__all__ = ['ReviewServiceDep',
           'MovieRatingServiceDep']
