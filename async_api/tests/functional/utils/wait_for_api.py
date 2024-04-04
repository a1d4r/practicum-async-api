import logging

import backoff
import httpx

from tests.functional.settings import settings
from tests.functional.utils.logger import setup_logger

logger = logging.getLogger(__name__)


@backoff.on_exception(backoff.expo, httpx.HTTPError, max_time=60)
def check_api_health():
    response = httpx.get(f"{settings.api_url}/health", timeout=1)
    response.raise_for_status()


def wait_for_api():
    logger.info("Waiting for API: %s", settings.api_url)
    check_api_health()
    logger.info("API is ready")


if __name__ == "__main__":
    setup_logger()
    wait_for_api()
