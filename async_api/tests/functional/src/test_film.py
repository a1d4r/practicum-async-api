import pytest

from elasticsearch import AsyncElasticsearch
from tests.functional.settings import settings


@pytest.mark.usefixtures("_create_indexes")
async def test_dummy(es_client: AsyncElasticsearch):
    assert await es_client.indices.exists(index=settings.es_films_index)
    assert await es_client.indices.exists(index=settings.es_genres_index)
    assert await es_client.indices.exists(index=settings.es_persons_index)
