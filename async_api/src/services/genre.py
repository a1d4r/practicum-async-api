from typing import Annotated

from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.settings import settings
from db.elastic import get_elasticsearch
from models.genre import Genre
from models.value_objects import GenreID


@dataclass
class GenreService:
    elastic: Annotated[AsyncElasticsearch, Depends(get_elasticsearch)]

    async def get_by_id(self, genre_id: GenreID) -> Genre | None:
        try:
            doc = await self.elastic.get(index=settings.es_genres_index, id=str(genre_id))
        except NotFoundError:
            return None
        return Genre.model_validate(doc["_source"])

    async def get_all(self) -> list[Genre]:
        result = await self.elastic.search(
            query={"match_all": {}},
        )
        return [Genre.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]
