from typing import Annotated

from api.dependencies import PaginationParams
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from models.value_objects import FilmID, PersonID, Roles
from pydantic import BaseModel, Field
from services.person import PersonService

router = APIRouter()


class PersonFilmShort(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    roles: list[Roles]


class PersonFilmDetailed(PersonFilmShort):
    title: str
    imdb_rating: float


class PersonDetails(BaseModel):
    uuid: PersonID = Field(..., validation_alias="id")
    full_name: str
    films: list[PersonFilmShort]


@router.get(
    "/search",
    response_model=list[PersonDetails],
    response_description="Список персон",
    status_code=status.HTTP_200_OK,
    summary="Поиск по персонам",
)
@cache(expire=60)
async def search_persons(
    person_service: Annotated[PersonService, Depends()],
    pagination_params: Annotated[PaginationParams, Depends()],
    query: str | None = None,
) -> list[PersonDetails]:
    persons = await person_service.search(
        query=query,
        page=pagination_params.page_number,
        size=pagination_params.page_size,
    )
    return [PersonDetails.model_validate(person.model_dump()) for person in persons]


@router.get(
    "/{person_id}",
    response_model=PersonDetails,
    response_description="Информация о персоне",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о персоне",
)
@cache(expire=60)
async def get_person_details(
    person_id: PersonID,
    person_service: Annotated[PersonService, Depends()],
) -> PersonDetails:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return PersonDetails.model_validate(person.model_dump())


@router.get(
    "/{person_id}/films",
    response_model=list[PersonFilmDetailed],
    response_description="Список фильмов, в которых участвовала персона",
    status_code=status.HTTP_200_OK,
    summary="Получить список фильмов, в которых участвовала персона",
)
@cache(expire=60)
async def get_person_films(
    person_id: PersonID,
    person_service: Annotated[PersonService, Depends()],
) -> list[PersonFilmDetailed]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return [PersonFilmDetailed.model_validate(film.model_dump()) for film in person.films]
