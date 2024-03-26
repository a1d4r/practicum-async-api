from typing import Annotated

from hashlib import sha256

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache import cache_insert, caches
from models.value_objects import GenreID
from pydantic import BaseModel, Field
from services.genre import GenreService

router = APIRouter()


class GenreDetails(BaseModel):
    uuid: GenreID = Field(..., validation_alias="id")
    name: str
    description: str | None = None


def get_cache_key_id(genre_id: GenreID, genre_service: GenreDetails) -> str:
    key = f"genre_details_{genre_id}_{genre_service.name}"
    return sha256(key.encode()).hexdigest()


def get_cache_key() -> str:
    key = "genres_list_cache_key"
    return sha256(key.encode()).hexdigest()


@router.get(
    "/{genre_id}",
    response_model=GenreDetails,
    response_description="Информация о жанре",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о жанре",
)
@cache_insert(key_func=get_cache_key_id, ttl=300, cache=caches["redis"])
async def get_genre_details(
    genre_id: GenreID,
    genre_service: Annotated[GenreService, Depends()],
) -> GenreDetails:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found"
        )
    return GenreDetails.model_validate(genre.model_dump())


@router.get(
    "/",
    response_model=list[GenreDetails],
    response_description="Список жанров",
    status_code=status.HTTP_200_OK,
    summary="Получить список всех жанров",
)
@cache_insert(key_func=get_cache_key, ttl=300, cache=caches["redis"])
async def get_genres_list(
    genre_service: Annotated[GenreService, Depends()],
) -> list[GenreDetails]:
    genres = await genre_service.get_all()
    return [GenreDetails.model_validate(genre.model_dump()) for genre in genres]
