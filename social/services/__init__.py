from typing import Annotated
from fastapi import Depends
from services.reviews import ReviewService
from services.rating import MovieRatingService

ReviewServiceDep = Annotated[ReviewService, Depends()]
MovieRatingServiceDep = Annotated[MovieRatingService, Depends()]

__all__ = ['ReviewServiceDep',
           'MovieRatingServiceDep']
