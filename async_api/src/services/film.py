from typing import Any

from functools import lru_cache

from db.elastic import get_elastic

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Document, Search
from fastapi import Depends
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    """Сервис для хранения и получения данных о фильме через Redis и Elasticsearch."""

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def all_films(self, **kwargs: dict[str, Any]) -> list[Film]:
        films = await self._get_films_from_elasticsearch(**kwargs)
        if not films:
            return []

        return films

    def get_all_films_from_elasticsearch(
        self,
        page_size: int = 10,
        page: int = 1,
        sort_by: str = "title",
        genre: str | None = None,
        query: str | None = None,
    ) -> dict | None:
        films = Search(using=get_elastic(), index="movies")
        if not films:
            return None
        if genre:
            films = films.filter("term", genre=genre)

        if query:
            films = films.query("match", title=query)

        films = films.sort({sort_by: {"order": "asc"}})
        response = films[(page - 1) * page_size : page * page_size].execute()

        return [hit.to_dict() for hit in response.hits]

    @staticmethod
    async def get_film_by_id(self, film_id: str) -> Film | None:
        film = await self._get_film_from_elasticsearch(film_id)
        if not film:
            return None

        return film

    async def _get_film_from_elasticsearch(self, film_id: str) -> Film:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return Film.model_validate(doc["_source"])

    async def _get_films_from_elasticsearch(self, model: Document) -> list[Document]:
        films_search = Search(index="movies").using(get_elastic()).doc_type(model)
        if not films_search:
            return None
        films_response = films_search.execute()

        return list(films_response)


@lru_cache
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
