from models.value_objects import FilmID, PersonID
from pydantic import BaseModel


class PersonFilm(BaseModel):
    """Модель для хранения информации о фильме, в котором участвовал актёр."""

    id: FilmID
    title: str
    imdb_rating: float
    roles: list[str]


class Person(BaseModel):
    """Модель для хранения информации об актёре."""

    id: PersonID
    full_name: str
    films: list[PersonFilm]
