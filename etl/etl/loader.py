import dataclasses

from collections.abc import Sequence

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
    def _load_records(self, index: str, records: Sequence[dto.BaseElasticsearchRecord]) -> None:
        """Загружает в данные в заданный индекс."""
        logger.info(
            "Going to insert {} documents into Elasticsearch",
            len(records),
        )
        helpers.bulk(
            self._client,
            [
                {"_index": index, "_id": str(record.id), "_source": dataclasses.asdict(record)}
                for record in records
            ],
        )
        logger.info(
            "Inserted {} documents into Elasticsearch",
            len(records),
        )

    @retry
    def load_film_works_records(
        self,
        film_works_records: list[dto.FilmWorkElasticsearchRecord],
    ) -> None:
        """Загружает в индекс данные о фильмах."""
        self._load_records("movies", film_works_records)

    @retry
    def load_genres_records(self, genres_records: list[dto.GenreElasticsearchRecord]) -> None:
        """Загружает в индекс данные о жанрах."""
        self._load_records("genres", genres_records)

    @retry
    def load_persons_records(self, persons_records: list[dto.PersonElasticsearchRecord]) -> None:
        """Загружает в индекс данные о персонах."""
        self._load_records("persons", persons_records)
