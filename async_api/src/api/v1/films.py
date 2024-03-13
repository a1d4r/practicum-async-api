from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Film(BaseModel):
    id: str
    title: str


@router.get("/{film_id}", response_model=Film)
async def film_details(film_id: str = "0") -> Film:
    return Film(id=film_id, title="some_title")
