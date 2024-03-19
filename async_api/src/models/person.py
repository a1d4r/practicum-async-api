from models.base import UUIDBase
from pydantic import Field


class PersonFilmRoles(UUIDBase):
    """Модель для хранения информации о ролях актёра в фильме."""

    roles: list[str]


class Person(UUIDBase):
    """Модель для хранения актёра."""

    full_name: str = Field(alias="name")
    films: list[PersonFilmRoles]
