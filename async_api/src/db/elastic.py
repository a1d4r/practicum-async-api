from core import config
from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch(
    [{"host": config.ELASTIC_HOST, "port": config.ELASTIC_PORT, "scheme": config.ELASTIC_SCHEME}],
)


class GetElasticError(Exception):
    def __init__(self, message: str = "Ellastic not found"):
        self.message = message


async def get_elastic() -> AsyncElasticsearch:
    es: AsyncElasticsearch | None = None
    if es is None:
        raise GetElasticError
    return es
