from typing import ClassVar

from src.models.genre import Genre
from src.models.mixins import OrjsonConfigMixin, UUIDMixin
from src.models.person import Person


class Film(UUIDMixin, OrjsonConfigMixin):
    title: str
    imdb_rating: float
    description: str = ""
    genre: ClassVar[list[Genre]] = []
    actors: ClassVar[list[Person]] = []
    writers: ClassVar[list[Person]] = []
    directors: ClassVar[list[Person]] = []
