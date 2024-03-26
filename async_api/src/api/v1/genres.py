from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from pydantic import BaseModel, Field

from core.settings import settings
from models.value_objects import GenreID
from services.genre import GenreService

router = APIRouter()


class GenreDetailsSchema(BaseModel):
    uuid: GenreID = Field(..., validation_alias="id")
    name: str
    description: str | None = None


@router.get(
    "/{genre_id}",
    response_model=GenreDetailsSchema,
    response_description="Информация о жанре",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о жанре",
)
@cache(expire=settings.ttl)
async def get_genre_details(
    genre_id: GenreID,
    genre_service: Annotated[GenreService, Depends()],
) -> GenreDetailsSchema:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return GenreDetailsSchema.model_validate(genre.model_dump())


@router.get(
    "/",
    response_model=list[GenreDetailsSchema],
    response_description="Список жанров",
    status_code=status.HTTP_200_OK,
    summary="Получить список всех жанров",
)
@cache(expire=settings.ttl)
async def get_genres_list(
    genre_service: Annotated[GenreService, Depends()],
) -> list[GenreDetailsSchema]:
    genres = await genre_service.get_all()
    return [GenreDetailsSchema.model_validate(genre.model_dump()) for genre in genres]
