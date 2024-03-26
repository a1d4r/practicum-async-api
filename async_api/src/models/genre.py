from pydantic import BaseModel

from models.value_objects import GenreID


class Genre(BaseModel):
    """Модель для хранения информации жанре в кинопроизведении."""

    id: GenreID
    name: str
    description: str | None = None
