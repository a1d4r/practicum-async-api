from models.base import UUIDBase
from models.film import FilmWorkMinimal
from pydantic import Field


class Person(UUIDBase):
    """Модель для хранения актёра."""

    full_name: str = Field(alias="name")
    films: list[FilmWorkMinimal]
