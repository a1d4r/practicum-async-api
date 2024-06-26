from pathlib import Path

import tenacity

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from tenacity import wait_random_exponential

PROJECT_ROOT = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Настройки приложения."""

    state_file_path: Path = PROJECT_ROOT / "state.json"
    log_level: str = "INFO"

    # Database
    postgres_dsn: PostgresDsn
    elasticsearch_host: str

    # Jobs run configuration
    persons_per_run: int = 100
    genres_per_run: int = 1
    film_works_per_run: int = 1000

    persons_run_interval: int = 60  # in seconds
    genres_run_interval: int = 60  # in seconds
    film_works_run_interval: int = 60  # in seconds

    # Retries
    retry_max_delay: float = 60.0  # in seconds
    retry_min_delay: float = 1.0  # in seconds
    retry_multiplier: float = 2

    ttl: int = 300

    @property
    def retry_policy(self) -> wait_random_exponential:
        """Randomly wait up to `retry_multiplier`^x * `retry_min_delay` seconds
        between each retry until the range reaches retry_max_delay seconds,
        then randomly up to `retry_max_delay` seconds afterwards.
        """
        return tenacity.wait_random_exponential(
            multiplier=self.retry_multiplier,
            min=self.retry_min_delay,
            max=self.retry_max_delay,
        )


settings = Settings(_env_file=PROJECT_ROOT / ".env")
