from api.v1 import films, genres, persons
from core.settings import settings
from db import elastic, redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=settings.api_project_name,
    root_path="/api",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup() -> None:
    await redis.redis.initialize()
    await elastic.es.info()


@app.on_event("shutdown")
async def shutdown() -> None:
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/v1/films", tags=["Фильмы"])
app.include_router(persons.router, prefix="/v1/persons", tags=["Персоны"])
app.include_router(genres.router, prefix="/v1/genres", tags=["Жанры"])
