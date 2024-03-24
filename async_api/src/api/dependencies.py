from core.settings import settings
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page_number: int = Field(1, ge=1)
    page_size: int = Field(settings.default_page_size, ge=1)
