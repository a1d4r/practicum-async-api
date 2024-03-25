from typing import Annotated

from hashlib import sha256

from api.dependencies import PaginationParams, SortParams
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache import cache_insert, caches
from models.value_objects import FilmID
from pydantic import BaseModel, Field
from services.film import FilmService

router = APIRouter()


class FilmShort(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    title: str
    imdb_rating: float


class IdName(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    name: str


class FilmDetails(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    title: str
    imdb_rating: float
    description: str | None = None
    genres: list[IdName]
    actors: list[IdName]
    writers: list[IdName]
    directors: list[IdName]


def get_cache_key(
    film_service: FilmShort,
    pagination_params: PaginationParams,
    query: str,
) -> str:
    key = f"{film_service.title}-{pagination_params.page_number}-{pagination_params.page_size}-{query}"
    return sha256(key.encode()).hexdigest()


def get_cache_key_id(film_id: FilmID, film_service: FilmDetails) -> str:
    key = f"film_details_{film_id}_{film_service.title}"
    return sha256(key.encode()).hexdigest()


@router.get(
    "/",
    response_model=list[FilmShort],
    response_description="Список фильмов",
    status_code=status.HTTP_200_OK,
    summary="Получить список всех фильмов",
)
@cache_insert(key_func=get_cache_key, ttl=300, cache=caches["redis"])
async def get_film_list(
    film_service: Annotated[FilmService, Depends()],
    pagination_params: Annotated[PaginationParams, Depends()],
    sort_params: Annotated[SortParams, Depends()],
    genre: str | None = None,
) -> list[FilmShort]:
    films = await film_service.get_list(
        page=pagination_params.page_number,
        size=pagination_params.page_size,
        sort_by=sort_params.sort_by,
        sort_order=sort_params.sort_order,
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
@cache_insert(key_func=get_cache_key, ttl=300, cache=caches["redis"])
async def search_films(
    film_service: Annotated[FilmService, Depends()],
    pagination_params: Annotated[PaginationParams, Depends()],
    query: str | None = None,
) -> list[FilmShort]:
    films = await film_service.search(
        query=query,
        page=pagination_params.page_number,
        size=pagination_params.page_size,
    )
    return [FilmShort.model_validate(film.model_dump()) for film in films]


@router.get(
    "/{film_id}",
    response_model=FilmDetails,
    response_description="Информация о фильме",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о фильме",
)
@cache_insert(key_func=get_cache_key_id, ttl=300, cache=caches["redis"])
async def get_film_details(
    film_id: FilmID,
    film_service: Annotated[FilmService, Depends()],
) -> FilmDetails:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
    return FilmDetails.model_validate(film.model_dump())
