from uuid import UUID

import pytest

from services.film import FilmService


@pytest.fixture()
async def film_service(elastic):
    return FilmService(elastic)


async def test_get_film_by_id(film_service: FilmService):
    # Arrange
    python_wars_id = UUID("25515b8c-2580-11eb-adc1-0242ac120002")

    # Act
    film = film_service.get_film_by_id(python_wars_id)

    # Assert
    assert film is not None
    assert film.id == python_wars_id
    assert film.title == "Python Wars: Hidden API"


async def test_get_film_from_elasticsearch(film_service: FilmService):
    # Arrange
    python_wars_id = UUID("25515b8c-2580-11eb-adc1-0242ac120002")

    # Act
    film = film_service.get_film_elasticsearc(python_wars_id)

    # Assert
    assert film is not None
    assert film.id == python_wars_id
    assert film.title == "Python Wars: Hidden API"


async def test_get_films_from_elasticsearch(film_service: FilmService):
    # Arrange
    page = 1
    size = 1

    # Act
    films = film_service.get_films_from_elasticsearch(page, size)
    assert len(films) == size
