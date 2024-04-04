from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api import health
from api.v1 import films, genres, persons
from core.settings import settings
from db.elastic import elasticsearch
from db.redis import redis
from utils.cache import key_builder


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await redis.initialize()
    await elasticsearch.info()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache", key_builder=key_builder)
    yield
    await redis.close()
    await elasticsearch.close()


app = FastAPI(
    title=settings.api_project_name,
    root_path="/api",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
app.include_router(health.router, tags=["Статус"])
app.include_router(films.router, prefix="/v1/films", tags=["Фильмы"])
app.include_router(persons.router, prefix="/v1/persons", tags=["Персоны"])
app.include_router(genres.router, prefix="/v1/genres", tags=["Жанры"])
