from typing import Annotated

from api.dependencies import PaginationParams
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models.genre import Genre
from models.person import Person
from models.value_objects import FilmID
from pydantic import BaseModel, Field
from services.film import FilmService

router = APIRouter()


class FilmShort(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    title: str
    imdb_rating: float


class FilmDetails(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    title: str
    imdb_rating: float
    description: str
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]


@router.get(
    "/",
    response_model=list[FilmShort],
    response_description="Список фильмов",
    status_code=status.HTTP_200_OK,
    summary="Получить список всех фильмов",
)
async def film_list(
    film_service: Annotated[FilmService, Depends()],
    pagination_params: Annotated[PaginationParams, Depends()],
    sort_by: str = Query("id", description="Сортировка фильмов"),
    genre: str = Query("Action", description="Фильтрация по жанру"),
) -> list[FilmShort]:
    films = await film_service.search_with_genre(
        page=pagination_params.page_number,
        size=pagination_params.page_size,
        sort_by=sort_by,
        genre=genre,
    )
    return [FilmShort.model_validate(film.model_dump()) for film in films]


@router.get(
    "/search",
    response_model=list[FilmShort],
    response_description="Список фильмов",
    status_code=status.HTTP_200_OK,
    summary="Поиск по фильмам",
)
async def film_search(
    film_service: Annotated[FilmService, Depends()],
    pagination_params: Annotated[PaginationParams, Depends()],
    sort_by: str = Query("id", description="Сортировка фильмов"),
    query: str | None = None,
) -> list[FilmShort]:
    films = await film_service.search(
        query=query,
        page=pagination_params.page_number,
        size=pagination_params.page_size,
        sort_by=sort_by,
    )
    return [FilmShort.model_validate(film.model_dump()) for film in films]


@router.get(
    "/{film_id}",
    response_model=FilmDetails,
    response_description="Информация о фильме",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о фильме",
)
async def get_film_details(
    film_id: FilmID,
    film_service: Annotated[FilmService, Depends()],
) -> FilmDetails:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
    return FilmDetails.model_validate(film.model_dump())
