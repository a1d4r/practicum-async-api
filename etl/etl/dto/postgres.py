from typing import Literal

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

__all__ = [
    "PersonIdModified",
    "GenreIdModified",
    "FilmWorkIdModified",
    "GenreInfo",
    "PersonInfo",
    "PersonFilmWorkRecord",
    "FilmWorkInfo",
    "FilmWorkGenreRecord",
    "FilmWorkPersonRecord",
]


@dataclass
class IdModified:
    """DTO для записей из БД с идентификатором и датой изменения."""

    id: UUID
    modified: datetime


class PersonIdModified(IdModified):
    pass


class GenreIdModified(IdModified):
    pass


class FilmWorkIdModified(IdModified):
    pass


@dataclass
class GenreInfo:
    """Информация о жанре."""

    id: UUID
    name: str
    description: str
    created: datetime
    modified: datetime


@dataclass
class PersonInfo:
    """Информация о персоне."""

    id: UUID
    full_name: str
    created: datetime
    modified: datetime


@dataclass
class PersonFilmWorkRecord:
    """Информация о фильме и ролях, в котором участвовала персона."""

    person_id: UUID
    film_work_id: UUID
    roles: list[str]


@dataclass
class FilmWorkInfo:
    """Информация о кинопроизведении."""

    id: UUID
    title: str
    description: str
    creation_date: str
    rating: float
    type: Literal["movie", "tv_show"]
    created: datetime
    modified: datetime


@dataclass
class FilmWorkGenreRecord:
    """Связь между кинопроизведением и жанром."""

    film_work_id: UUID
    genre_id: UUID
    genre_name: str


@dataclass
class FilmWorkPersonRecord:
    """Информация о персоне, участвовавшей в кинопроизведении."""

    film_work_id: UUID
    person_id: UUID
    person_full_name: str
    role: str
