from models.base import UUIDBase


class PersonFilm(UUIDBase):
    """Модель для хранения информации о фильме, в котором участвовал актёр."""

    title: str
    imdb_rating: float
    roles: list[str]


class Person(UUIDBase):
    """Модель для хранения информации об актёре."""

    full_name: str
    films: list[PersonFilm]
