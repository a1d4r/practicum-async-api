from dataclasses import dataclass

from models.base import UUIDBase
from models.person import Person, PersonName


@dataclass
class Film(UUIDBase):
    """Модель для хранения информации о фильме."""

    title: str
    imdb_rating: float | None
    description: str | None
    director: list[str] | None
    actors_names: list[str]
    writers_names: list[str]
    actors: list[PersonName]
    writers: list[PersonName]


class FilmMinimal(UUIDBase):
    """Модель для хранения краткой информации о фильме."""

    title: str
    imdb_rating: float
    description: str
    writers: list[Person]
    directors: list[Person]


class FilmShort(UUIDBase):
    """Модель для хранения краткой информации о фильме на главной странице."""

    title: str
    imdb_rating: float
