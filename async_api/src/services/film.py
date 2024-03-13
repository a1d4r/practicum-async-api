# nfrom typing import Optional
import sys

sys.path.append("async_api/src/models/")

from functools import lru_cache

# nfrom db.elastic import get_elastic
# nfrom db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

# nfrom fastapi import Depends
from src.models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Film | None:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _film_from_cache(self, film_id: str) -> Film | None:
        data = await self.redis.get(film_id)
        if not data:
            return None

        return Film.parse_raw(data)

    async def _put_film_to_cache(self, film: Film) -> None:
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache
def get_film_service(
    redis: Redis,
    elastic: AsyncElasticsearch,
) -> FilmService:
    return FilmService(redis, elastic)
