from typing import cast

from random import Random

from faker import Faker
from polyfactory.decorators import post_generated
from polyfactory.factories.pydantic_factory import ModelFactory

from models.film import Film, GenreIdName, PersonIdName
from models.genre import Genre
from models.person import Person, PersonFilm

GENRES = [
    "Action",
    "Adventure",
    "Fantasy",
    "Drama",
    "Comedy",
    "Horror",
    "Romance",
]


class PersonFilmFactory(ModelFactory[PersonFilm]):
    __faker__ = Faker()
    __set_as_default_factory_for_type__ = True

    __randomize_collection_length__ = True
    __min_collection_length__ = 1
    __max_collection_length__ = 4

    @classmethod
    def title(cls) -> str:
        return cast(str, cls.__faker__.sentence(nb_words=3))

    @classmethod
    def imdb_rating(cls):
        return cast(str, cls.__faker__.random.uniform(1.0, 10.0))


class PersonFactory(ModelFactory[Person]):
    __faker__ = Faker()
    __set_as_default_factory_for_type__ = True

    __randomize_collection_length__ = True
    __min_collection_length__ = 1
    __max_collection_length__ = 4

    @classmethod
    def full_name(cls) -> str:
        return cast(str, cls.__faker__.name())


class PersonIdNameFactory(ModelFactory[PersonIdName]):
    __faker__ = Faker()
    __set_as_default_factory_for_type__ = True

    @classmethod
    def name(cls) -> str:
        return cast(str, cls.__faker__.name())


class GenreIdNameFactory(ModelFactory[GenreIdName]):
    __random__ = Random()
    __set_as_default_factory_for_type__ = True

    @classmethod
    def name(cls) -> str:
        return cls.__random__.choice(GENRES)


class GenreFactory(ModelFactory[Genre]):
    __random__ = Random()
    __set_as_default_factory_for_type__ = True

    @classmethod
    def name(cls) -> str:
        return cls.__random__.choice(GENRES)

    @classmethod
    def description(cls) -> str:
        return cast(str, cls.__faker__.sentence(nb_words=10))


class FilmFactory(ModelFactory[Film]):
    __faker__ = Faker()
    __model__ = Film

    __randomize_collection_length__ = True
    __min_collection_length__ = 1
    __max_collection_length__ = 4

    @classmethod
    def title(cls) -> str:
        return cast(str, cls.__faker__.sentence(nb_words=3))

    @classmethod
    def description(cls) -> str:
        return cast(str, cls.__faker__.sentence(nb_words=10))

    @classmethod
    def imdb_rating(cls):
        return cast(str, cls.__faker__.random.uniform(1.0, 10.0))

    @post_generated
    @classmethod
    def directors_names(cls, directors: list[PersonIdName]) -> list[str]:
        return [director.name for director in directors]

    @post_generated
    @classmethod
    def actors_names(cls, actors: list[PersonIdName]) -> list[str]:
        return [actor.name for actor in actors]

    @post_generated
    @classmethod
    def writers_names(cls, writers: list[PersonIdName]) -> list[str]:
        return [writer.name for writer in writers]
