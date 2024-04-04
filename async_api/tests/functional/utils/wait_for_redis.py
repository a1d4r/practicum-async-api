import logging

import backoff

from redis import Redis

from tests.functional.settings import settings
from tests.functional.utils.logger import setup_logger

logger = logging.getLogger(__name__)


@backoff.on_predicate(backoff.expo, max_time=60)
def check_redis_health():
    redis = Redis.from_url(str(settings.redis_url), socket_timeout=1)
    return redis.ping()


def wait_for_redis():
    logger.info("Waiting for redis: %s", settings.redis_url)
    check_redis_health()
    logger.info("Redis is ready")


if __name__ == "__main__":
    setup_logger()
    wait_for_redis()
