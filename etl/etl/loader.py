import dataclasses

import elastic_transport
import tenacity

from elasticsearch import Elasticsearch, helpers
from loguru import logger

from etl import dto
from etl.settings import settings

retry = tenacity.retry(
    before_sleep=tenacity.before_sleep_log(logger, "ERROR"),  # type: ignore[arg-type]
    after=tenacity.after_log(logger, "INFO"),  # type: ignore[arg-type]
    retry=tenacity.retry_if_exception_type(elastic_transport.ConnectionError),
    wait=settings.retry_policy,
)


class ElasticsearchLoader:
    def __init__(self, client: Elasticsearch) -> None:
        self._client = client

    @retry
    def load_film_works_records(
        self,
        film_works_records: list[dto.FilmWorkElasticsearchRecord],
    ) -> None:
        """Загружает в индекс данные о фильмах."""
        helpers.bulk(
            self._client,
            [
                {"_index": "movies", "_id": str(record.id), "_source": dataclasses.asdict(record)}
                for record in film_works_records
            ],
        )
