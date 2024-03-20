from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from loguru import logger
from typing import List, Type


from models.film import FilmWork, FilmMinimal, FilmShort, FilmWorkMinimal
from redis.asyncio import Redis
from services.utils import get_key_by_args

from elasticsearch_dsl import Search, Document

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    """Сервис для хранения и получения данных о фильме через Redis и Elasticsearch."""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def all_films(self, **kwargs) -> list[FilmWork]:
        films = await self._films_work_from_cache(**kwargs)
        if not films:
            films = await self._get_films_from_elastic(FilmWork)
            if not films:
                return []
            await self._put_films_to_cache(FilmWork)
        return films

    def get_all_films_from_elasticsearch(
        page_size=10, page=1, sort_by="title", genre=None, query=None
    ):
        films = Search(get_elastic())
        if not films:
            return
        if genre:
            films = films.filter("term", genre=genre)

        if query:
            films = films.query("match", title=query)

        films = films.sort({sort_by: {"order": "asc"}})
        response = films[(page - 1) * page_size : page * page_size].execute()
        films = [hit.to_dict() for hit in response.hits]

        return films

    @staticmethod
    async def get_film_by_id(self, film_id: str) -> FilmWork | None:
        film = await self._film_from_work_cache(film_id)
        if not film:
            film = await self._get_film_from_elasticsearch(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elasticsearch(self, film_id: str) -> FilmWork | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return FilmWork(**doc["_source"])

    async def _get_films_from_elasticsearch(self, model: Type[Document]) -> List[Document]:
        try:
            films_work_search = Search(index="movies").using(get_elastic())
            films_work_response = films_work_search.execute()
        except NotFoundError:
            return None
        return [hit for hit in films_work_response]

    async def _film_from_cache(self, film_id: str) -> FilmWork | None:
        data = await self.redis.get(f"films:{film_id}")
        if not data:
            return None

        return FilmWork.parse_raw(data)

    async def _film_from_cache(self, film_id: str) -> FilmWork:
        data = await self.redis.get(film_id)
        if not data:
            logger.debug(f"The film was not found in the cache (id: {film_id})")
            return None

        film = FilmWork.parse_raw(data)

        return film

    async def _films_from_cache(self, **kwargs) -> list[FilmWork]:
        key = await get_key_by_args(**kwargs)
        data = await self.redis.get(key)
        if not data:
            logger.debug("FilmWork was not found in the cache")
            return None

        return [FilmWork.parse_raw(item) for item in data]

    async def _put_film_to_cache(self, film: FilmWork) -> None:
        await self.redis.set(film.id, film, FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_films_to_cache(self, films: list[FilmWork], **search_params):
        key = await get_key_by_args(**search_params)
        films_data = [film.dict(by_alias=True) for film in films]
        await self.redis.set(key, films_data, ex=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
