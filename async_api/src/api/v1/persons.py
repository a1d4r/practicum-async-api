from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from models.value_objects import FilmID, PersonID, Roles
from pydantic import BaseModel, Field

from services.person import PersonService

router = APIRouter()


class PersonFilm(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    roles: list[Roles]


class PersonDetails(BaseModel):
    uuid: PersonID = Field(..., validation_alias="id")
    full_name: str
    films: list[PersonFilm]


@router.get(
    "/{person_id}",
    response_model=PersonDetails,
    response_description="Информация о персоне",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о персоне",
)
async def get_person_details(
    person_id: PersonID,
    person_service: Annotated[PersonService, Depends()],
) -> PersonDetails:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return PersonDetails.model_validate(person.model_dump())
