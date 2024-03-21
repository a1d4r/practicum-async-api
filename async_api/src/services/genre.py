from typing import Annotated, NewType

from dataclasses import dataclass
from uuid import UUID

from core.settings import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.genre import Genre

GenreID = NewType("GenreID", UUID)


@dataclass
class GenreService:
    elastic: Annotated[AsyncElasticsearch, Depends(get_elastic)]

    async def get_by_id(self, genre_id: GenreID) -> Genre | None:
        try:
            doc = await self.elastic.get(index=settings.es_genres_index, id=str(genre_id))
        except NotFoundError:
            return None
        return Genre.model_validate(doc["_source"])

    async def search(
        self,
        page: int = 1,
        size: int = settings.default_page_size,
    ) -> list[Genre]:
        result = await self.elastic.search(
            index=settings.es_genres_index,
            from_=(page - 1) * size,
            size=size,
            query={"match_all": {}},
        )
        return [Genre.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]
