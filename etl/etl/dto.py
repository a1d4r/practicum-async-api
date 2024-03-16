from typing import Literal

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


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
    """Связь между кинопроизведением и персоной."""

    film_work_id: UUID
    person_id: UUID
    person_full_name: str
    role: str


@dataclass
class PersonElasticsearchRecord:
    """Объект для хранения информации о персоне в индексе Elasticsearch."""

    id: UUID
    name: str


@dataclass
class FilmWorkElasticsearchRecord:
    """Объект для хранения информации о кинопроизведении в индексе Elasticsearch."""

    id: UUID
    imdb_rating: float
    genre: list[str]
    title: str
    description: str
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[PersonElasticsearchRecord]
    writers: list[PersonElasticsearchRecord]
