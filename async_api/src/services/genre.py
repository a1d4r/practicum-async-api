from typing import Annotated

from abc import ABC, abstractmethod

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import Depends

from core.settings import settings
from db.elastic import get_elasticsearch
from models.genre import Genre
from models.value_objects import GenreID


class BaseGenreService(ABC):
    @abstractmethod
    async def get_or_none(self, genre_id: GenreID) -> Genre | None:
        pass

    @abstractmethod
    async def get_list(self) -> list[Genre]:
        pass


class ElasticsearchGenreService(BaseGenreService):
    def __init__(self, elastic: Annotated[AsyncElasticsearch, Depends(get_elasticsearch)]):
        self.elastic = elastic

    async def get_or_none(self, genre_id: GenreID) -> Genre | None:
        try:
            doc = await self.elastic.get(index=settings.es_genres_index, id=str(genre_id))
            return Genre.model_validate(doc["_source"])
        except NotFoundError:
            return None

    async def get_list(self) -> list[Genre]:
        result = await self.elastic.search(
            query={"match_all": {}},
        )
        return [Genre.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]
