from typing import NewType, dict, list

from functools import lru_cache
from uuid import UUID

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
FilmID = NewType("FilmID", UUID)


class FilmService:
    """Сервис для хранения и получения данных о фильме через Redis и Elasticsearch."""

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def films(self, **kwargs: dict[str, str]) -> list[Film]:
        films = await self.get_films_from_elasticsearch(**kwargs)
        if not films:
            return []

        return films

    def get_films_from_elasticsearch(
        self,
        page_size: int = 10,
        page: int = 1,
        sort_order: str = "asc",
        genre: str | None = None,
        query: str | None = None,
    ) -> dict | None:
        films = []
        if not self.elastic:
            return None
        if genre:
            films = [
                hit
                for hit in self.elastic.search(
                    index="movies",
                    body={
                        "query": {
                            "bool": {
                                "filter": [
                                    {"term": {"genre": genre}},
                                    {"match": {"title": query}},
                                ],
                            },
                        },
                        "sort": [{"{sort_by}": {sort_order}}],
                        "from": (page - 1) * page_size,
                        "size": page_size,
                    },
                ).hits
            ]
        else:
            films = [
                hit
                for hit in self.elastic.search(
                    index="movies",
                    body={
                        "query": {"match_all": {}},
                        "sort": [{"{sort_by}": {sort_order}}],
                        "from": (page - 1) * page_size,
                        "size": page_size,
                    },
                ).hits
            ]

        return [hit.to_dict() for hit in films]

    async def get_film_by_id(self, film_id: FilmID) -> Film | None:
        film = await self.get_film_from_elasticsearch(FilmID(film_id))
        if not film:
            return None

        return film

    async def get_film_from_elasticsearch(self, film_id: FilmID) -> Film:
        try:
            doc = await self.elastic.get(index="movies", id=str(film_id))
        except NotFoundError:
            return None
        return Film.model_validate(doc["_source"])


@lru_cache
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
