from pydantic import BaseModel, Field


class UUIDBase(BaseModel):
    id: str = Field(alias="id")
