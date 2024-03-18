from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from loguru import logger

from models.film import FilmWork, FilmMinimal, FilmShort, FilmWorkMinimal
from redis.asyncio import Redis
from services.utils import get_key_by_args

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    """Сервис для хранения и получения данных о фильме через Redis и Elasticsearch."""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def all_films_work(self, **kwargs) -> list[FilmWork]:
        films = await self._films_work_from_cache(**kwargs)
        if not films:
            films = await self._get_film(**kwargs)
            if not films:
                return []
            await self._put_films_wo_to_cache(films, **kwargs)
        return films

    @staticmethod
    async def _make_person_from_elasticsearch_doc(doc: dict):
        pass

    async def _get_person_from_elasticsearch(self, person_id: str):
        pass

    async def _get_persons_from_elasticsearch(self, **kwargs):
        pass

    async def _person_from_cache(self, person_id: str):
        pass

    async def _persons_from_cache(self, **kwargs):
        pass

    async def _put_person_to_cache(self, person):
        pass

    async def get_film_by_id(self, film_id: str) -> FilmWork | None:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def get_film_minimal_by_id(self, film_id: str) -> FilmMinimal | None:
        film = await self._film_minimal_from_cache(film_id)
        if not film:
            film = await self._get_film_minimal_from_elasticsearch(film_id)
            if not film:
                return None
            await self._put_film_minimal_to_cache(film)

        return film

    async def get_film_short_by_id(self, film_id: str) -> FilmShort | None:
        film = await self._film_short_from_cache(film_id)
        if not film:
            film = await self._get_film_short_from_elasticsearch(film_id)
            if not film:
                return None
            await self._put_film_short_to_cache(film)

        return film

    async def get_film_work_minimal(self, film_id: str) -> FilmWorkMinimal | None:
        film = await self._film_work_minimal_from_cache(film_id)
        if not film:
            film = await self._get_film_work_minimal_from_elasticsearch(film_id)
            if not film:
                return None
            await self._put_film_work_minimal_to_cache(film)

        return film

    async def _get_film_from_elasticsearch(self, film_id: str) -> FilmWork | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return FilmWork(**doc["_source"])

    async def _get_films_from_elastic(self, **kwargs) -> list[FilmWork]:
        try:
            films_work_search = Search(index="movies").using(get_elastic())
            films_work_response = films_work_search.execute()
        except NotFoundError:
            return None
        return [hit for hit in films_work_response]

    async def _get_film_minimal_from_elasticsearch(self, film_id: str) -> FilmMinimal | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return FilmMinimal(**doc["_source"])

    async def _get_film_short_from_elasticsearch(self, film_id: str) -> FilmShort | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return FilmShort(**doc["_source"])

    async def _get_film_work_minimal_from_elasticsearch(
        self, film_id: str
    ) -> FilmWorkMinimal | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return FilmWorkMinimal(**doc["_source"])

    async def _film_work_from_cache(self, film_id: str) -> FilmWork | None:
        data = await self.redis.get(film_id)
        if not data:
            return None

        return FilmWork.parse_raw(data)

    async def _film_minimal_from_cache(self, film_id: str) -> FilmMinimal | None:
        data = await self.redis.get(film_id)
        if not data:
            return None

        return FilmMinimal.parse_raw(data)

    async def _film_short_from_cache(self, film_id: str) -> FilmShort | None:
        data = await self.redis.get(film_id)
        if not data:
            return None

        return FilmShort.parse_raw(data)

    async def _film_work_minimal_from_cache(self, film_id: str) -> FilmWorkMinimal | None:
        data = await self.redis.get(film_id)
        if not data:
            return None

        return FilmWorkMinimal.parse_raw(data)

    async def _films_work_from_cache(self, **kwargs) -> list[FilmWork]:
        key = await get_key_by_args(**kwargs)
        data = await self.redis.get(key)
        if not data:
            logger.debug("FilmWork was not found in the cache")
            return None

        return [FilmWork.parse_raw(item) for item in data]

    async def _films_minimal_from_cache(self, **kwargs) -> list[FilmMinimal]:
        key = await get_key_by_args(**kwargs)
        data = await self.redis.get(key)
        if not data:
            logger.debug("FilmMinimal was not found in the cache")
            return None

        return [FilmMinimal.parse_raw(item) for item in data]

    async def _films_short_from_cache(self, **kwargs) -> list[FilmShort]:
        key = await get_key_by_args(**kwargs)
        data = await self.redis.get(key)
        if not data:
            logger.debug("FilmShort was not found in the cache")
            return None

        return [FilmShort.parse_raw(item) for item in data]

    async def _films_work_minimal_from_cache(self, **kwargs) -> list[FilmWorkMinimal]:
        key = await get_key_by_args(**kwargs)
        data = await self.redis.get(key)
        if not data:
            logger.debug("FilmWorkMinimal was not found in the cache")
            return None

        return [FilmWorkMinimal.parse_raw(item) for item in data]

    async def _put_film_to_cache(self, film: FilmWork) -> None:
        await self.redis.set(film.id, film, FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_film_minimal_to_cache(self, film: FilmWorkMinimal) -> None:
        await self.redis.set(film.id, film, FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_film_short_to_cache(self, film: FilmShort) -> None:
        await self.redis.set(film.id, film, FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_film_work_minimal_to_cache(self, film: FilmWorkMinimal) -> None:
        await self.redis.set(film.id, film, FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
