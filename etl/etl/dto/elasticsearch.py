from dataclasses import dataclass
from uuid import UUID

__all__ = [
    "BaseElasticsearchRecord",
    "PersonMinimalElasticsearchRecord",
    "FilmWorkMinimalElasticsearchRecord",
    "GenreElasticsearchRecord",
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
class FilmWorkMinimalElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения краткой информации о кинопроизведении в индексе Elasticsearch."""

    roles: list[str]


@dataclass
class GenreElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения информации о жанре в индексе Elasticsearch."""

    name: str
    description: str


@dataclass
class PersonElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения информации о персоне в индексе Elasticsearch."""

    full_name: str
    films: list[FilmWorkMinimalElasticsearchRecord]


@dataclass
class FilmWorkElasticsearchRecord(BaseElasticsearchRecord):
    """Модель для хранения информации о кинопроизведении в индексе Elasticsearch."""

    imdb_rating: float
    genre: list[str]
    title: str
    description: str
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[PersonMinimalElasticsearchRecord]
    writers: list[PersonMinimalElasticsearchRecord]
