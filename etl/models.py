import uuid
from pydantic import Field, BaseModel


class UUIDMixin(BaseModel):
    id: uuid.UUID


class PersonList(UUIDMixin):
    full_name: str


class Genre(UUIDMixin):
    name: str


class Movie(UUIDMixin):
    imdb_rating: float | None = Field(None, ge=0, le=100)
    title: str
    description: str | None
    genre: list[Genre] | None
    directors: list[PersonList] | None
    actors: list[PersonList] | None
    writers: list[PersonList] | None


class Person(PersonList):
    films: list


map_models = {
    'film_work': Movie,
    'genre': Genre,
    'person': Person,
}


