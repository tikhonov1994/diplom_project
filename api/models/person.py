from models.base import Base, IndexItemList


class PersonFilmWorkRelation(Base):
    roles: list[str]


class PersonFilmWork(Base):
    title: str
    imdb_rating: float


class BasePerson(Base):
    full_name: str


class Person(BasePerson):
    films: list[PersonFilmWorkRelation]


class PersonList(IndexItemList):
    results: list[Person]
