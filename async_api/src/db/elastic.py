from core.settings import settings
from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch(settings.elasticsearch_host)


def get_elastic() -> AsyncElasticsearch:
    return es
