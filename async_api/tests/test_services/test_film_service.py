from uuid import UUID

import pytest

from models.film import Film
from services.film import FilmService


@pytest.fixture()
async def film_service(elastic):
    return FilmService(elastic)


async def test_search_film_by_id(film_service):
    # Arrange
    star_wars_id = UUID("c35dc09c-8ace-46be-8941-7e50b768ec33")

    # Act
    film = await film_service.get_by_id(star_wars_id)

    # Assert
    assert film is not None
    assert film.id == star_wars_id
    assert film.title == "Star Wars"
    assert film.imdb_rating == 6.6
    assert (
        film.description
        == "Luke Skywalker, a young farmer from the desert planet of Tattooine, must save Princess Leia from the evil Darth Vader."
    )
    assert film.genre == ["Action", "Fantasy", "Adventure"]
    assert film.actors == []
    assert film.writers == [{"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas"}]
    assert film.directors == []


async def test_search_films(film_service):
    # Arrange
    page = 2
    size = 5

    # Act
    films = await film_service.search(page, size)

    # Assert
    assert len(films) == size
    assert all(isinstance(film, Film) for film in films)
