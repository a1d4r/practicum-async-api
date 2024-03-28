import logging
import time

import httpx

from tests.functional.settings import settings
from tests.functional.utils.logger import setup_logger

logger = logging.getLogger(__name__)


def wait_for_api():
    logger.info("Waiting for API: %s", settings.api_url)
    while True:
        try:
            response = httpx.get(f"{settings.api_url}/health", timeout=1)
        except httpx.ConnectError:
            time.sleep(1)
            continue
        if response.status_code == 200:
            break
        time.sleep(1)
    logger.info("API is ready")


if __name__ == "__main__":
    setup_logger()
    wait_for_api()
