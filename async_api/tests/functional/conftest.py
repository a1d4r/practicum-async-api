import pytest

from elasticsearch import AsyncElasticsearch
from httpx import AsyncClient
from redis.asyncio import Redis

from tests.functional.settings import settings


@pytest.fixture()
async def es_client():
    es = AsyncElasticsearch(settings.elasticsearch_host)
    yield es
    await es.close()


@pytest.fixture(scope="session")
async def redis_client():
    redis = Redis.from_url(str(settings.redis_url))
    yield redis
    await redis.close()


@pytest.fixture(scope="session", autouse=True)
async def _reset_cache(redis_client: Redis):
    await redis_client.flushdb()
    yield
    await redis_client.flushdb()


@pytest.fixture(autouse=True)
async def _create_indexes(es_client: AsyncElasticsearch):
    for es_index in (settings.es_genres_index, settings.es_persons_index, settings.es_films_index):
        if await es_client.indices.exists(index=es_index):
            await es_client.indices.delete(index=es_index)
        await es_client.indices.create(index=es_index)


@pytest.fixture()
async def test_client():
    async with AsyncClient(base_url=settings.api_url) as client:
        yield client
