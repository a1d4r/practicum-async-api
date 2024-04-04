from typing import Annotated

from abc import ABC, abstractmethod

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import Depends

from core.settings import settings
from db.elastic import get_elasticsearch
from models.person import Person
from models.value_objects import PersonID


class BasePersonService(ABC):
    @abstractmethod
    async def get_or_none(self, person_id: PersonID) -> Person | None:
        pass

    @abstractmethod
    async def search(
        self,
        *,
        query: str | None = None,
        page: int = 1,
        size: int = settings.default_page_size,
    ) -> list[Person]:
        pass


class ElasticsearchPersonService(BasePersonService):
    def __init__(self, elastic: Annotated[AsyncElasticsearch, Depends(get_elasticsearch)]):
        self.elastic = elastic

    async def get_or_none(self, person_id: PersonID) -> Person | None:
        try:
            doc = await self.elastic.get(index=settings.es_persons_index, id=str(person_id))
        except NotFoundError:
            return None
        return Person.model_validate(doc["_source"])

    async def search(
        self,
        *,
        query: str | None = None,
        page: int = 1,
        size: int = settings.default_page_size,
    ) -> list[Person]:
        search_query = {"match": {"full_name": query}} if query else {"match_all": {}}
        result = await self.elastic.search(
            index=settings.es_persons_index,
            from_=(page - 1) * size,
            size=size,
            query=search_query,
        )
        return [Person.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]
