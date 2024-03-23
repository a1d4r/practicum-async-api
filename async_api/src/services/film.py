from typing import Annotated, NewType

from dataclasses import dataclass
from uuid import UUID

from core.settings import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
FilmID = NewType("FilmID", UUID)


@dataclass
class FilmService:
    elastic: Annotated[AsyncElasticsearch, Depends(get_elastic)]

    async def search(
        self,
        *,
        query: str | None = None,
        page: int = 1,
        size: int = settings.default_page_size,
        sort_order: str | None = "asc",
        sort_by: str = "id",
        genre: str = "Action",
    ) -> list[Film]:
        result = await self.elastic.search(
            index=settings.es_films_index,
            from_=(page - 1) * size,
            size=size,
            query={"match": {"title": query}} if query else {"match_all": {}},
            sort={sort_by: {"order": sort_order, "genre": genre}},
        )

        return [Film.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]

    async def get_by_id(self, film_id: FilmID) -> Film | None:
        try:
            doc = await self.elastic.get(index=settings.es_films_index, id=str(film_id))
        except NotFoundError:
            return None
        return Film.model_validate(doc["_source"])
