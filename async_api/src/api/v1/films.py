from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.film import FilmID, FilmService

router = APIRouter()


class Film(BaseModel):
    id: UUID
    title: str


@router.get("/{film_id}", response_model=Film)
async def film_details(film_id: FilmID, film_service: FilmService = Depends()) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return Film(id=film.id, title=film.title)
