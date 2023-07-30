from typing import Optional

from models.base import Base, IndexItemList
from models.genre import Genre
from models.person import BasePerson


class Film(Base):
    title: str
    description: Optional[str]
    imdb_rating: Optional[float]
    genre: list[Genre] = []
    director: list[BasePerson] = []
    actors: list[BasePerson] = []
    writers: list[BasePerson] = []


class FilmList(IndexItemList):
    results = list[Film]
