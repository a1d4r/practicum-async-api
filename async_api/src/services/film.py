from typing import Annotated

from dataclasses import dataclass
from functools import lru_cache

from core.settings import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film
from models.value_objects import FilmID

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


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
        sort_by: str = "id",
    ) -> list[Film]:
        result = await self.elastic.search(
            index=settings.es_films_index,
            from_=(page - 1) * size,
            size=size,
            query={"match": {"title": query}} if query else {"match_all": {}},
            sort={sort_by: {"order": sort_order}},
        )

        return [Film.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]

    async def search_with_genre(
        self,
        *,
        page: int = 1,
        size: int = settings.default_page_size,
        sort_by: str = "imdb_rating",
        sort_order: str = "desc",
        genre: str | None = "Action",
    ) -> list[Film]:
        result = await self.elastic.search(
            index=settings.es_films_index,
            from_=(page - 1) * size,
            size=size,
            query={"term": {"genre": genre}},
            sort={sort_by: {"order": sort_order}},
        )

        return [Film.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]

    async def get_by_id(self, film_id: FilmID) -> Film | None:
        try:
            doc = await self.elastic.get(index=settings.es_films_index, id=str(film_id))
        except NotFoundError:
            return None
        return Film.model_validate(doc["_source"])


@lru_cache
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
