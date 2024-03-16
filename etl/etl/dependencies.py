import contextlib

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime

import psycopg
import tenacity

from elasticsearch import Elasticsearch
from loguru import logger
from psycopg.rows import DictRow, dict_row

from etl.extractor import PostgresExtractor
from etl.loader import ElasticsearchLoader
from etl.pipeline import ETL
from etl.settings import settings
from etl.state import ETLState, StateManager
from etl.storage.file_storage import JsonFileStorage


def get_state_manager() -> StateManager[ETLState]:
    storage = JsonFileStorage(settings.state_file_path)
    datetime_min = datetime.min.replace(tzinfo=UTC)
    return StateManager(
        storage,
        ETLState,
        ETLState(
            persons_modified_cursor=datetime_min,
            genres_modified_cursor=datetime_min,
            film_works_modified_cursor=datetime_min,
        ),
    )


@contextmanager
def get_pg_connection() -> Iterator[psycopg.Connection[DictRow]]:
    for attempt in tenacity.Retrying(
        before_sleep=tenacity.before_sleep_log(logger, "ERROR"),  # type: ignore[arg-type]
        after=tenacity.after_log(logger, "INFO"),  # type: ignore[arg-type]
        retry=tenacity.retry_if_exception_type(psycopg.OperationalError),
        wait=settings.retry_policy,
    ):
        with (
            attempt,
            contextlib.closing(
                psycopg.connect(str(settings.postgres_dsn), row_factory=dict_row),
            ) as pg_conn,
        ):
            logger.debug("Connecting to PostgreSQL...")
            yield pg_conn


@contextmanager
def get_es_connection() -> Iterator[Elasticsearch]:
    with contextlib.closing(Elasticsearch(settings.elasticsearch_host)) as es_client:
        yield es_client


@contextmanager
def get_etl() -> Iterator[ETL]:
    with get_pg_connection() as pg_conn, get_es_connection() as es_client:
        extractor = PostgresExtractor(pg_conn)
        loader = ElasticsearchLoader(es_client)
        state_manager = get_state_manager()
        yield ETL(state_manager, extractor, loader, settings)
