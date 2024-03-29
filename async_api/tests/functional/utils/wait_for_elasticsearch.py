import logging
import time

from elasticsearch import Elasticsearch

from tests.functional.settings import settings
from tests.functional.utils.logger import setup_logger

logger = logging.getLogger(__name__)


def wait_for_elasticsearch():
    es_client = Elasticsearch(settings.elasticsearch_host, request_timeout=1)
    logger.info("Waiting for elasticsearch: %s", settings.elasticsearch_host)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
    logger.info("Elasticsearch is ready")


if __name__ == "__main__":
    setup_logger()
    wait_for_elasticsearch()
