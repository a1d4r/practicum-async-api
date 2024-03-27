from typing import Annotated

from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.settings import settings
from db.elastic import get_elasticsearch
from models.person import Person
from models.value_objects import PersonID


@dataclass
class PersonService:
    elastic: Annotated[AsyncElasticsearch, Depends(get_elasticsearch)]

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
        result = await self.elastic.search(
            index=settings.es_persons_index,
            from_=(page - 1) * size,
            size=size,
            query={"match": {"full_name": query}} if query else {"match_all": {}},
        )
        return [Person.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]
