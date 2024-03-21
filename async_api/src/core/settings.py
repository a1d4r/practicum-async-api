from pathlib import Path

from pydantic import RedisDsn
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    api_project_name: str = "Movies"

    # cache
    redis_url: RedisDsn

    # elasticsearch
    elasticsearch_host: str
    es_genres_index: str = "genres"
    es_persons_index: str = "persons"

    # pagination
    default_page_size: int = 50


settings = Settings(_env_file=PROJECT_ROOT / ".env")
