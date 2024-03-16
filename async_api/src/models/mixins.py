from pydantic import BaseModel, Field


class UUIDMixin(BaseModel):
    uuid: str = Field(alias="id")


class OrjsonConfigMixin(BaseModel):
    class Config:
        pass
