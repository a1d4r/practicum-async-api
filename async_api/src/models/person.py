from models.base import UUIDBase


class PersonFilm(UUIDBase):
    """Модель для хранения информации о фильме, в котором участвовал актёр."""

    title: str
    imdb_rating: float
    roles: list[str]


class PersonFilmRoles(UUIDBase):
    """Модель для хранения информации о ролях актёра в фильме."""

    title: str
    imdb_rating: float
    roles: list[str]


class Person(UUIDBase):
    """Модель для хранения информации об актёре."""

    full_name: str
    films: list[PersonFilmRoles]


class PersonService(UUIDBase):
    full_name: str
    imdb_rating: float

    films: list[PersonFilmRoles]


class PersonName(UUIDBase):
    name: str
