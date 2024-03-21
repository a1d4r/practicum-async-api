from typing import Any, dict, list

from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Document, Search
from fastapi import Depends
from loguru import logger
from models.film import FilmWork
from redis.asyncio import Redis
from services.utils import get_key_by_args

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    """Сервис для хранения и получения данных о фильме через Redis и Elasticsearch."""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def all_films(self, **kwargs: dict[str, Any]) -> list[FilmWork]:
        films = await self._films_from_cache(**kwargs)
        if not films:
            films = await self._get_films_from_elasticsearch(FilmWork)
            if not films:
                return []
            await self._put_films_to_cache(FilmWork)
        return films

    def get_all_films_from_elasticsearch(
        self,
        page_size: int = 10,
        page: int = 1,
        sort_by: str = "title",
        genre: str | None = None,
        query: str | None = None,
    ) -> dict | None:
        films = Search(get_elastic())
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
    async def get_film_by_id(self, film_id: str) -> FilmWork | None:
        try:
            film = await self._film_from_work_cache(film_id)
        except NotFoundError:
            film = await self._get_film_from_elasticsearch(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elasticsearch(self, film_id: str) -> FilmWork:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return FilmWork(**doc["_source"])

    async def _get_films_from_elasticsearch(self, model: Document) -> list[Document]:
        try:
            films_search = Search(index="movies").using(get_elastic()).doc_type(model)
            films_response = films_search.execute()
        except NotFoundError:
            return None
        return [hit for hit in films_response]

    async def _film_from_cache(self, film_id: str) -> FilmWork | None:
        data = await self.redis.get(f"films:{film_id}")
        if not data:
            return None

        return FilmWork.parse_raw(data)

    async def _films_from_cache(self, **kwargs: dict[str, Any]) -> list[FilmWork]:
        key = await get_key_by_args(**kwargs)
        data = await self.redis.get(key)
        if not data:
            logger.debug("FilmWork was not found in the cache")
            return None

        return [FilmWork.parse_raw(item) for item in data]

    async def _put_film_to_cache(self, film: FilmWork) -> None:
        await self.redis.set(film.id, film, FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_films_to_cache(self, films: list[FilmWork], **search_params: str | Any) -> None:
        key = await get_key_by_args(**search_params)
        films_data = [film.dict(by_alias=True) for film in films]
        await self.redis.set(key, str(films_data), ex=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
