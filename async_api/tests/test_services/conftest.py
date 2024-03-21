import pytest

from services.genre import GenreService


@pytest.fixture()
async def genre_service(elastic):
    return GenreService(elastic)
