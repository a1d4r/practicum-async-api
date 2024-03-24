from models.value_objects import GenreID
from pydantic import BaseModel


class Genre(BaseModel):
    """Модель для хранения информации жанре в кинопроизведении."""

    id: GenreID
    name: str
    description: str | None = None
