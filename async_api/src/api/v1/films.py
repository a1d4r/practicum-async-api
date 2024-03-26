from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from pydantic import BaseModel, Field

from api.dependencies import PaginationParams, SortParams
from core.settings import settings
from models.value_objects import FilmID
from services.film import FilmService

router = APIRouter()


class FilmShortSchema(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    title: str
    imdb_rating: float


class IdNameSchema(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    name: str


class FilmDetailsSchema(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    title: str
    imdb_rating: float
    description: str | None = None
    genres: list[IdNameSchema]
    actors: list[IdNameSchema]
    writers: list[IdNameSchema]
    directors: list[IdNameSchema]


@router.get(
    "/",
    response_model=list[FilmShortSchema],
    response_description="Список фильмов",
    status_code=status.HTTP_200_OK,
    summary="Получить список всех фильмов",
)
@cache(expire=settings.cache_ttl_seconds)
async def get_film_list(
    film_service: Annotated[FilmService, Depends()],
    pagination_params: Annotated[PaginationParams, Depends()],
    sort_params: Annotated[SortParams, Depends()],
    genre: str | None = None,
) -> list[FilmShortSchema]:
    films = await film_service.get_list(
        page=pagination_params.page_number,
        size=pagination_params.page_size,
        sort_by=sort_params.sort_by,
        sort_order=sort_params.sort_order,
        genre=genre,
    )
    return [FilmShortSchema.model_validate(film.model_dump()) for film in films]


@router.get(
    "/search",
    response_model=list[FilmShortSchema],
    response_description="Список фильмов",
    status_code=status.HTTP_200_OK,
    summary="Поиск по фильмам",
)
@cache(expire=settings.cache_ttl_seconds)
async def search_films(
    film_service: Annotated[FilmService, Depends()],
    pagination_params: Annotated[PaginationParams, Depends()],
    query: str | None = None,
) -> list[FilmShortSchema]:
    films = await film_service.search(
        query=query,
        page=pagination_params.page_number,
        size=pagination_params.page_size,
    )
    return [FilmShortSchema.model_validate(film.model_dump()) for film in films]


@router.get(
    "/{film_id}",
    response_model=FilmDetailsSchema,
    response_description="Информация о фильме",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о фильме",
)
@cache(expire=settings.cache_ttl_seconds)
async def get_film_details(
    film_id: FilmID,
    film_service: Annotated[FilmService, Depends()],
) -> FilmDetailsSchema:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
    return FilmDetailsSchema.model_validate(film.model_dump())
