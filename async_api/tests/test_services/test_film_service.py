from uuid import UUID

import pytest

from models.film import Film
from models.value_objects import FilmID
from services.film import FilmService


@pytest.fixture()
async def film_service(elastic, redis):
    return FilmService(elastic, redis)


async def test_search_film_by_id(film_service: FilmService):
    # Arrange
    star_wars_id = FilmID(UUID("c35dc09c-8ace-46be-8941-7e50b768ec33"))

    # Act
    film = await film_service.get_by_id(star_wars_id)
    # Assert
    assert film is not None
    assert film.id == star_wars_id
    assert film.imdb_rating == 6.6
    assert film.title == "Star Wars"
    assert (
        film.description
        == "Luke Skywalker, a young farmer from the desert planet of Tattooine, must save Princess Leia from the evil Darth Vader."
    )
    assert film.directors == []
    assert film.actors_names == []
    assert film.writers_names == ["George Lucas"]
    assert film.actors == []
    assert film.writers[0].id == UUID("a5a8f573-3cee-4ccc-8a2b-91cb9f55250a")
    assert film.writers[0].name == "George Lucas"


async def test_search_films(film_service: FilmService):
    # Arrange
    page = 2
    size = 5

    # Act
    films = await film_service.search(page=page, size=size)

    # Assert
    assert len(films) == size
    assert all(isinstance(film, Film) for film in films)


async def test_get_films_by_genre(film_service: FilmService):
    # Act
    films = await film_service.get_list(genre="Action")

    # Assert
    assert len(films) is not None


async def test_put_film_to_cache(film_service: FilmService):
    # Arrange
    star_wars_id = FilmID(UUID("c35dc09c-8ace-46be-8941-7e50b768ec33"))
    # n film = await film_service.get_by_id(star_wars_id)

    # Act
    await film_service.put_film_to_cache(
        Film(
            id=star_wars_id,
            imdb_rating=6.6,
            title="Star Wars",
            description="Luke Skywalker, a young farmer from the desert planet of Tattooine, must save Princess Leia from the evil Darth Vader.",
            directors=[],
            actors_names=[],
            writers_names=["George Lucas"],
            actors=[],
            writers=[],
            genres=[],
            directors_names=[],
        ),
    )

    get_film = await film_service.get_film_by_id_from_cache(star_wars_id)

    # Assert

    assert get_film is not None
