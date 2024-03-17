from models.film import FilmWorkMinimal
from models.mixins import UUIDBase
from pydantic import Field


class Person(UUIDBase):
    """Модель для хранения актёра."""

    full_name: str = Field(alias="name")
    films: list[FilmWorkMinimal]
