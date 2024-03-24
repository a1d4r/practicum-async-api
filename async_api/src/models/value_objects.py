from typing import NewType

from uuid import UUID

# Алиасы для идентификаторов
GenreID = NewType("GenreID", UUID)
PersonID = NewType("PersonID", UUID)
FilmID = NewType("FilmID", UUID)
