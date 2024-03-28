from pathlib import Path

from pydantic import RedisDsn
from pydantic_settings import BaseSettings

FUNC_TESTS_ROOT = Path(__file__).parent


class Settings(BaseSettings):
    redis_url: RedisDsn
    elasticsearch_host: str
    es_genres_index: str = "genres"
    es_persons_index: str = "persons"
    es_films_index: str = "movies"

    # pagination
    default_page_size: int = 50


settings = Settings(_env_file=FUNC_TESTS_ROOT / ".env.test")
