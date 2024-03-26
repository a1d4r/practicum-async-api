from enum import StrEnum, auto

from pydantic import BaseModel

from models.value_objects import FilmID, PersonID


class PersonIdName(BaseModel):
    """Модель для хранения идентификатора и имени актёра."""

    id: PersonID
    name: str


class GenreIdName(BaseModel):
    """Модель для хранения идентификатора и имени жанра."""

    id: FilmID
    name: str


class Film(BaseModel):
    """Модель для хранения информации о фильме."""

    id: FilmID
    title: str
    imdb_rating: float | None
    description: str | None
    genres: list[GenreIdName]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[PersonIdName]
    writers: list[PersonIdName]
    directors: list[PersonIdName]


class FilmSortFields(StrEnum):
    id = auto()
    imdb_rating = auto()
    title = auto()  # type: ignore[assignment]
