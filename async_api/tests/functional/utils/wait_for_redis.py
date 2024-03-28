import logging
import time

from redis import Redis
from tests.functional.settings import settings
from tests.functional.utils.logger import setup_logger

logger = logging.getLogger(__name__)


def wait_for_redis():
    redis = Redis.from_url(str(settings.redis_url), socket_timeout=1)
    logger.info("Waiting for redis: %s", settings.redis_url)
    while True:
        if redis.ping():
            break
        time.sleep(1)
    logger.info("Redis is ready")


if __name__ == "__main__":
    setup_logger()
    wait_for_redis()
