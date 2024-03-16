from core import config
from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch(
    [{"host": config.ELASTIC_HOST, "port": config.ELASTIC_PORT, "scheme": config.ELASTIC_SCHEME}],
)


async def get_elastic() -> AsyncElasticsearch:
    return es
