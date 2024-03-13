# nfrom typing import Optional

from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch | None = None


class GetElasticError(Exception):
    def __init__(self, message: str = "Ellastic not found"):
        self.message = message


async def get_elastic() -> AsyncElasticsearch:
    es: AsyncElasticsearch | None = None
    if es is None:
        raise GetElasticError
    return es
