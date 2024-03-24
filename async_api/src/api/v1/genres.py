from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from models.value_objects import GenreID
from pydantic import BaseModel, Field
from services.genre import GenreService

router = APIRouter()


class GenreDetails(BaseModel):
    uuid: GenreID = Field(..., validation_alias="id")
    name: str
    description: str | None = None


@router.get(
    "/{genre_id}",
    response_model=GenreDetails,
    response_description="Информация о жанре",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о жанре",
)
async def get_genre_details(
    genre_id: GenreID,
    genre_service: Annotated[GenreService, Depends()],
) -> GenreDetails:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return GenreDetails.model_validate(genre.model_dump())


@router.get(
    "/",
    response_model=list[GenreDetails],
    response_description="Список жанров",
    status_code=status.HTTP_200_OK,
    summary="Получить список всех жанров",
)
async def get_genres_list(
    genre_service: Annotated[GenreService, Depends()],
) -> list[GenreDetails]:
    genres = await genre_service.get_all()
    return [GenreDetails.model_validate(genre.model_dump()) for genre in genres]
