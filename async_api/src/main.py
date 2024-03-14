import os

import uvicorn

from api.v1 import films
from core import config
from db import elastic, redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.PROJECT_NAME,
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


app.include_router(films.router, prefix="/v1/films", tags=["films"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=str(os.getenv("HOST")),
        port=8000,
    )
