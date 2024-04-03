from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from api.dependencies import PaginationParams
from api.v1.schemas.persons import PersonDetailsSchema, PersonFilmDetailedSchema
from core.settings import settings
from models.person import Person, PersonFilm
from models.value_objects import PersonID
from services.person import BasePersonService, ElasticsearchPersonService

router = APIRouter()


@router.get(
    "/search",
    response_model=list[PersonDetailsSchema],
    response_description="Список персон",
    status_code=status.HTTP_200_OK,
    summary="Поиск по персонам",
)
@cache(expire=settings.cache_ttl_seconds)
async def search_persons(
    person_service: Annotated[BasePersonService, Depends(ElasticsearchPersonService)],
    pagination_params: Annotated[PaginationParams, Depends()],
    query: str | None = None,
) -> list[Person]:
    return await person_service.search(
        query=query,
        page=pagination_params.page_number,
        size=pagination_params.page_size,
    )


@router.get(
    "/{person_id}",
    response_model=PersonDetailsSchema,
    response_description="Информация о персоне",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о персоне",
)
@cache(expire=settings.cache_ttl_seconds)
async def get_person_details(
    person_id: PersonID,
    person_service: Annotated[BasePersonService, Depends(ElasticsearchPersonService)],
) -> Person:
    person = await person_service.get_or_none(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person


@router.get(
    "/{person_id}/films",
    response_model=list[PersonFilmDetailedSchema],
    response_description="Список фильмов, в которых участвовала персона",
    status_code=status.HTTP_200_OK,
    summary="Получить список фильмов, в которых участвовала персона",
)
@cache(expire=settings.cache_ttl_seconds)
async def get_person_films(
    person_id: PersonID,
    person_service: Annotated[BasePersonService, Depends(ElasticsearchPersonService)],
) -> list[PersonFilm]:
    person = await person_service.get_or_none(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person.films
