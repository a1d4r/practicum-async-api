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
        sort_order: str = "asc",
        genre: str | None = None,
    ) -> list[Film]:
        if genre:
            result = await self.elastic.search(
                index=settings.es_films_index,
                from_=(page - 1) * size,
                size=size,
                query={"match": {"title": query}} if query else {"match_all": {}},
            )
        else:
            result = await self.elastic.search(
                index=settings.es_films_index,
                from_=(page - 1) * size,
                size=size,
                query={"match": {"title": query}} if query else {"match_all": {}},
                sort=sort_order,
            )

        return [Film.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]

    async def get_by_id(self, film_id: FilmID) -> Film | None:
        try:
            doc = await self.elastic.get(index="movies", id=str(film_id))
        except NotFoundError:
            return None
        return Film.model_validate(doc["_source"])


def get_film_service() -> None:
    return None
