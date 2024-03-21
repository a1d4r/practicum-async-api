from pathlib import Path

from pydantic import RedisDsn
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    api_project_name: str = "Movies"
    redis_url: RedisDsn
    elasticsearch_host: str

    # pagination
    default_page_size: int = 50

    # elasticsearch
    es_genres_index: str = "genres"


settings = Settings(_env_file=PROJECT_ROOT / ".env")
