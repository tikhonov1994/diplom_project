from typing import Annotated
from fastapi import Depends
from services.reviews import ReviewService


ReviewServiceDep = Annotated[ReviewService, Depends()]

__all__ = ['ReviewServiceDep']
