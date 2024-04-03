from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from api.dependencies import PaginationParams, SortParams
from api.v1.schemas.films import FilmDetailsSchema, FilmShortSchema
from core.settings import settings
from models.film import Film
from models.value_objects import FilmID
from services.film import BaseFilmService, ElasticsearchFilmService

router = APIRouter()


@router.get(
    "/",
    response_model=list[FilmShortSchema],
    response_description="Список фильмов",
    status_code=status.HTTP_200_OK,
    summary="Получить список всех фильмов",
)
@cache(expire=settings.cache_ttl_seconds)
async def get_film_list(
    film_service: Annotated[BaseFilmService, Depends(ElasticsearchFilmService)],
    pagination_params: Annotated[PaginationParams, Depends()],
    sort_params: Annotated[SortParams, Depends()],
    genre: str | None = None,
) -> list[Film]:
    return await film_service.get_list(
        page=pagination_params.page_number,
        size=pagination_params.page_size,
        sort_by=sort_params.sort_by,
        sort_order=sort_params.sort_order,
        genre=genre,
    )


@router.get(
    "/search",
    response_model=list[FilmShortSchema],
    response_description="Список фильмов",
    status_code=status.HTTP_200_OK,
    summary="Поиск по фильмам",
)
@cache(expire=settings.cache_ttl_seconds)
async def search_films(
    film_service: Annotated[BaseFilmService, Depends(ElasticsearchFilmService)],
    pagination_params: Annotated[PaginationParams, Depends()],
    query: str | None = None,
) -> list[Film]:
    return await film_service.search(
        query=query,
        page=pagination_params.page_number,
        size=pagination_params.page_size,
    )


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
    film_service: Annotated[BaseFilmService, Depends(ElasticsearchFilmService)],
) -> Film:
    film = await film_service.get_or_none(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
    return film
