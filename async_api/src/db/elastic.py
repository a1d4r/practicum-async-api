from elasticsearch import AsyncElasticsearch

from core.settings import settings

es = AsyncElasticsearch(settings.elasticsearch_host)


def get_elastic() -> AsyncElasticsearch:
    return es
