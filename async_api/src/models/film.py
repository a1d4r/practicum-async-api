from dataclasses import dataclass

from models.base import UUIDBase
from models.person import Person


@dataclass
class Film(UUIDBase):
    """Модель для хранения информации о фильме."""

    title: str
    imdb_rating: float
    description: str | None
    genre: list[str]
    actors: list[Person] | None
    writers: list[Person] | None
    directors: list[Person] | None


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
