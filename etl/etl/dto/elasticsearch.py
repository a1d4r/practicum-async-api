from dataclasses import dataclass
from uuid import UUID

__all__ = [
    "BaseElasticsearchRecord",
    "PersonMinimalElasticsearchRecord",
    "PersonFilmWorkElasticsearchRecord",
    "GenreElasticsearchRecord",
    "GenreMinimalElasticsearchRecord",
    "PersonElasticsearchRecord",
    "FilmWorkElasticsearchRecord",
]


@dataclass
class BaseElasticsearchRecord:
    """Базовая модель для хранения информации в индексе Elasticsearch."""

    id: UUID


@dataclass
class PersonMinimalElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения краткой информации о персоне в индексе Elasticsearch."""

    name: str


@dataclass
class PersonFilmWorkElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения информации о кинопроизведении,
    в котором участвовала персона, в индексе Elasticsearch.
    """

    title: str
    imdb_rating: float
    roles: list[str]


@dataclass
class GenreElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения информации о жанре в индексе Elasticsearch."""

    name: str
    description: str


@dataclass
class GenreMinimalElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения краткой информации о жанре в индексе Elasticsearch."""

    name: str


@dataclass
class PersonElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения информации о персоне в индексе Elasticsearch."""

    full_name: str
    films: list[PersonFilmWorkElasticsearchRecord]


@dataclass
class FilmWorkElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения информации о кинопроизведении в индексе Elasticsearch."""

    imdb_rating: float
    title: str
    description: str
    genres: list[GenreMinimalElasticsearchRecord]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[PersonMinimalElasticsearchRecord]
    actors: list[PersonMinimalElasticsearchRecord]
    writers: list[PersonMinimalElasticsearchRecord]
