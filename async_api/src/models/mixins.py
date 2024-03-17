from pydantic import BaseModel, Field


class UUIDBase(BaseModel):
    """Модель для базового класса."""

    id: str = Field(alias="id")
