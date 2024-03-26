from typing import NewType

from enum import StrEnum, auto
from uuid import UUID

# Алиасы для идентификаторов
GenreID = NewType("GenreID", UUID)
PersonID = NewType("PersonID", UUID)
FilmID = NewType("FilmID", UUID)


class Roles(StrEnum):
    """Роли персоны в фильме."""

    actor = auto()
    writer = auto()
    director = auto()


class SortOrder(StrEnum):
    asc = auto()
    desc = auto()
