from dataclasses import dataclass

from models.genre import Genre
from models.mixins import UUIDBase
from models.person import Person


@dataclass
class Film(UUIDBase):
    title: str
    imdb_rating: float
    description: str
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
