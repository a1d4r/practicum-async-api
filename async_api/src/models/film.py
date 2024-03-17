from dataclasses import dataclass

from models.genre import Genre
from models.mixins import UUIDBase
from models.person import Person


@dataclass
class FilmWork(UUIDBase):
    """Модель для хранения информации о фильме."""

    title: str
    imdb_rating: float
    description: str
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]


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


class FilmWorkMinimal(UUIDBase):
    """Модель для хранения краткой информации о кинопроизведении."""

    roles: list[str]
