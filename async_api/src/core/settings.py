from pathlib import Path

from pydantic import RedisDsn
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    api_project_name: str = "Movies"

    # cache
    redis_url: RedisDsn
    cache_ttl_seconds: int = 300

    # elasticsearch
    elasticsearch_host: str
    es_genres_index: str = "genres"
    es_persons_index: str = "persons"
    es_films_index: str = "movies"

    # pagination
    default_page_size: int = 50


settings = Settings(_env_file=PROJECT_ROOT / ".env")
