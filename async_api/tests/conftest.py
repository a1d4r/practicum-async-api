import pytest

from elasticsearch import AsyncElasticsearch

from core.settings import settings


@pytest.fixture()
async def elastic():
    es = AsyncElasticsearch(settings.elasticsearch_host)
    yield es
    await es.close()
