from typing import Annotated, NewType

from dataclasses import dataclass
from uuid import UUID

from core.settings import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.person import Person

PersonID = NewType("PersonID", UUID)


@dataclass
class PersonService:
    elastic: Annotated[AsyncElasticsearch, Depends(get_elastic)]

    async def get_by_id(self, person_id: UUID) -> Person | None:
        try:
            doc = await self.elastic.get(index=settings.es_persons_index, id=str(person_id))
        except NotFoundError:
            return None
        return Person.model_validate(doc["_source"])

    async def search(
        self,
        page: int = 1,
        size: int = settings.default_page_size,
    ) -> list[Person]:
        result = await self.elastic.search(
            index=settings.es_persons_index,
            from_=(page - 1) * size,
            size=size,
            query={"match_all": {}},
        )
        return [Person.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]
