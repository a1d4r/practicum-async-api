from elasticsearch import AsyncElasticsearch

from core.settings import settings

elasticsearch = AsyncElasticsearch(settings.elasticsearch_host)


def get_elasticsearch() -> AsyncElasticsearch:
    return elasticsearch
