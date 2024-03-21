from models.base import UUIDBase


class PersonFilmRoles(UUIDBase):
    """Модель для хранения информации о ролях актёра в фильме."""

    roles: list[str]


class Person(UUIDBase):
    """Модель для хранения информации об актёре."""

    full_name: str
    films: list[PersonFilmRoles]
