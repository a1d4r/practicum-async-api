import logging

import backoff

from elastic_transport import TransportError
from elasticsearch import ApiError, Elasticsearch

from tests.functional.settings import settings
from tests.functional.utils.logger import setup_logger

logging.getLogger("elastic_transport.transport").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


@backoff.on_exception(backoff.expo, (ApiError, TransportError), max_time=60)
def check_elasticsearch_health():
    es_client = Elasticsearch(settings.elasticsearch_host, request_timeout=1)
    es_client.info()


def wait_for_elasticsearch():
    logger.info("Waiting for elasticsearch: %s", settings.elasticsearch_host)
    check_elasticsearch_health()
    logger.info("Elasticsearch is ready")


if __name__ == "__main__":
    setup_logger()
    wait_for_elasticsearch()
