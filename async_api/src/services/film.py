from typing import Annotated

from abc import ABC, abstractmethod

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import Depends

from core.settings import settings
from db.elastic import get_elasticsearch
from models.film import Film
from models.value_objects import FilmID, SortOrder


class BaseFilmService(ABC):
    @abstractmethod
    async def get_list(
        self,
        *,
        page: int = 1,
        size: int = settings.default_page_size,
        sort_by: str | None = None,
        sort_order: SortOrder | None = None,
        genre: str | None = None,
    ) -> list[Film]:
        pass

    @abstractmethod
    async def search(
        self,
        *,
        query: str | None = None,
        page: int = 1,
        size: int = settings.default_page_size,
    ) -> list[Film]:
        pass

    @abstractmethod
    async def get_or_none(self, film_id: FilmID) -> Film | None:
        pass


class ElasticsearchFilmService(BaseFilmService):
    def __init__(self, elastic: Annotated[AsyncElasticsearch, Depends(get_elasticsearch)]):
        self.elastic = elastic

    async def get_list(
        self,
        *,
        page: int = 1,
        size: int = settings.default_page_size,
        sort_by: str | None = None,
        sort_order: SortOrder | None = None,
        genre: str | None = None,
    ) -> list[Film]:
        query: dict[str, dict[str, dict[str, str | dict[str, str]]]]
        query = {"match_all": {}}
        if genre:
            query = {"bool": {"filter": {"term": {"genres.name.keyword": genre}}}}

        sort = None
        if sort_by:
            sort = {sort_by: {"order": sort_order or SortOrder.asc}}

        result = await self.elastic.search(
            index=settings.es_films_index,
            from_=(page - 1) * size,
            size=size,
            query=query,
            sort=sort,
        )
        return [Film.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]

    async def search(
        self,
        *,
        query: str | None = None,
        page: int = 1,
        size: int = settings.default_page_size,
    ) -> list[Film]:
        result = await self.elastic.search(
            index=settings.es_films_index,
            from_=(page - 1) * size,
            size=size,
            query={"match": {"title": query}} if query else {"match_all": {}},
        )
        return [Film.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]

    async def get_or_none(self, film_id: FilmID) -> Film | None:
        try:
            doc = await self.elastic.get(index=settings.es_films_index, id=str(film_id))
            return Film.model_validate(doc["_source"])
        except NotFoundError:
            return None
