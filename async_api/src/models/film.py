from models.value_objects import FilmID, PersonID
from pydantic import BaseModel


class PersonIdName(BaseModel):
    """Модель для хранения идентификатора и имени актёра."""

    id: PersonID
    name: str


class Film(BaseModel):
    """Модель для хранения информации о фильме."""

    id: FilmID
    title: str
    imdb_rating: float | None
    description: str | None
    director: list[str] | None
    actors_names: list[str]
    writers_names: list[str]
    actors: list[PersonIdName]
    writers: list[PersonIdName]
