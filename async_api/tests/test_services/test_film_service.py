from uuid import UUID

import pytest

from models.film import Film
from services.film import FilmID, FilmService


@pytest.fixture()
async def film_service(elastic):
    return FilmService(elastic)


async def test_search_film_by_id(film_service):
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
    assert film.director == []
    assert film.actors_names == []
    assert film.writers_names == ["George Lucas"]
    assert film.actors == []
    assert film.writers[0].id == UUID("a5a8f573-3cee-4ccc-8a2b-91cb9f55250a")
    assert film.writers[0].name == "George Lucas"


async def test_search_persons(film_service: FilmService):
    # Arrange
    page = 2
    size = 5

    # Act
    films = await film_service.search(page=page, size=size)

    # Assert
    assert len(films) == size
    assert all(isinstance(film, Film) for film in films)
