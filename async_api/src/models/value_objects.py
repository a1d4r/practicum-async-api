from enum import auto, StrEnum
from typing import NewType

from uuid import UUID

# Алиасы для идентификаторов
GenreID = NewType("GenreID", UUID)
PersonID = NewType("PersonID", UUID)
FilmID = NewType("FilmID", UUID)


class Roles(StrEnum):
    actor = auto()
    writer = auto()
    director = auto()
