from typing import Annotated

from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.settings import settings
from db.elastic import get_elasticsearch
from models.film import Film
from models.value_objects import FilmID, SortOrder


@dataclass
class FilmService:
    elastic: Annotated[AsyncElasticsearch, Depends(get_elasticsearch)]

    async def get_list(
        self,
        *,
        page: int = 1,
        size: int = settings.default_page_size,
        sort_by: str | None = None,
        sort_order: SortOrder | None = None,
        genre: str | None = None,
    ) -> list[Film]:
        result = await self.elastic.search(
            index=settings.es_films_index,
            from_=(page - 1) * size,
            size=size,
            query=(
                {"bool": {"filter": {"term": {"genres.name.keyword": genre}}}}
                if genre
                else {"match_all": {}}
            ),
            sort={sort_by: {"order": sort_order or SortOrder.asc}} if sort_by else None,
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

    async def get_by_id(self, film_id: FilmID) -> Film | None:
        try:
            doc = await self.elastic.get(index=settings.es_films_index, id=str(film_id))
        except NotFoundError:
            return None
        return Film.model_validate(doc["_source"])
