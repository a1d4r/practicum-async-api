from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from api.v1.schemas.genres import GenreDetailsSchema
from core.settings import settings
from models.genre import Genre
from models.value_objects import GenreID
from services.genre import BaseGenreService, ElasticsearchGenreService

router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=GenreDetailsSchema,
    response_description="Информация о жанре",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о жанре",
)
@cache(expire=settings.cache_ttl_seconds)
async def get_genre_details(
    genre_id: GenreID,
    genre_service: Annotated[BaseGenreService, Depends(ElasticsearchGenreService)],
) -> Genre:
    genre = await genre_service.get_or_none(genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return genre


@router.get(
    "/",
    response_model=list[GenreDetailsSchema],
    response_description="Список жанров",
    status_code=status.HTTP_200_OK,
    summary="Получить список всех жанров",
)
@cache(expire=settings.cache_ttl_seconds)
async def get_genres_list(
    genre_service: Annotated[BaseGenreService, Depends(ElasticsearchGenreService)],
) -> list[Genre]:
    return await genre_service.get_list()
