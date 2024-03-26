from pydantic import BaseModel

from models.value_objects import FilmID, PersonID, Roles


class PersonFilm(BaseModel):
    """Модель для хранения информации о фильме, в котором участвовал актёр."""

    id: FilmID
    title: str
    imdb_rating: float
    roles: list[Roles]


class Person(BaseModel):
    """Модель для хранения информации об актёре."""

    id: PersonID
    full_name: str
    films: list[PersonFilm]
