import sys

from loguru import logger

from etl.jobs import scheduler
from etl.settings import settings

if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level=settings.log_level)
    scheduler.start()
