from models.mixins import UUIDBase


class Genre(UUIDBase):
    """Модель для хранения информации жанре в кинопроизведении."""

    name: str
    description: str


class GenreMinimal(UUIDBase):
    """Модель для хранения краткой информации о жанре."""

    name: str
