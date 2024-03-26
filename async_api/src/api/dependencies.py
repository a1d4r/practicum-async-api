from pydantic import BaseModel, Field

from core.settings import settings
from models.value_objects import SortOrder


class PaginationParams(BaseModel):
    page_number: int = Field(1, ge=1)
    page_size: int = Field(settings.default_page_size, ge=1)


class SortParams(BaseModel):
    sort: str | None = Field(None, min_length=1)

    @property
    def sort_by(self) -> str | None:
        if not self.sort:
            return None
        return self.sort.lstrip("-")

    @property
    def sort_order(self) -> SortOrder | None:
        if not self.sort:
            return None
        return SortOrder.desc if self.sort.startswith("-") else SortOrder.asc
