from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_project_name: str = "Movies"
    redis_url: RedisDsn
    elasticsearch_host: str


settings = Settings(_env_file=".env")
