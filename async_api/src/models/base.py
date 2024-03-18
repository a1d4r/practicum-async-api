from pydantic import BaseModel


class UUIDBase(BaseModel):
    """Модель для базового класса."""

    id: str
