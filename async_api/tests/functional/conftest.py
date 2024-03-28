import pytest

from elasticsearch import AsyncElasticsearch
from tests.functional.settings import settings


@pytest.fixture(scope="session")
async def es_client():
    es = AsyncElasticsearch(settings.elasticsearch_host)
    yield es
    await es.close()


@pytest.fixture()
async def _create_indexes(es_client: AsyncElasticsearch):
    for es_index in (settings.es_genres_index, settings.es_persons_index, settings.es_films_index):
        if await es_client.indices.exists(index=es_index):
            await es_client.indices.delete(index=es_index)
        await es_client.indices.create(index=es_index)
