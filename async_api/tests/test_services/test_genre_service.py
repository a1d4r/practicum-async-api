from uuid import UUID

import pytest

from models.genre import Genre
from models.value_objects import GenreID
from services.genre import GenreService


@pytest.fixture()
async def genre_service(elastic):
    return GenreService(elastic)


async def test_get_genre_by_id(genre_service: GenreService):
    # Arrange
    action_genre_id = GenreID(UUID("3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"))

    # Act
    genre = await genre_service.get_or_none(action_genre_id)

    # Assert
    assert genre is not None
    assert genre.id == action_genre_id
    assert genre.name == "Action"


async def test_get_all_genres(genre_service: GenreService):
    # Act
    genres = await genre_service.get_list()

    # Assert
    assert len(genres) == 10
    assert all(isinstance(genre, Genre) for genre in genres)
