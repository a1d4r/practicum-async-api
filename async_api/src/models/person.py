from models.mixins import UUIDBase
from pydantic import Field


class Person(UUIDBase):
    full_name: str = Field(alias="name")
