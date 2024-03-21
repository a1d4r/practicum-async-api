import pytest

from core.settings import settings
from elasticsearch import AsyncElasticsearch


@pytest.fixture()
async def elastic():
    es = AsyncElasticsearch(settings.elasticsearch_host)
    yield es
    await es.close()
