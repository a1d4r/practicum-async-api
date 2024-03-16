from datetime import UTC, datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from etl.dependencies import get_etl
from etl.settings import settings

scheduler = BlockingScheduler()


@scheduler.scheduled_job(
    "interval",
    seconds=settings.persons_run_interval,
    next_run_time=datetime.now(UTC),
)
def check_for_updated_persons() -> None:
    logger.info("Checking for updated persons")
    with get_etl() as etl:
        etl.synchronize_person_updates()


@scheduler.scheduled_job(
    "interval",
    seconds=settings.genres_run_interval,
    next_run_time=datetime.now(UTC) + timedelta(seconds=1),
)
def check_for_updated_genres() -> None:
    logger.info("Checking for updated genres")
    with get_etl() as etl:
        etl.synchronize_genre_updates()


@scheduler.scheduled_job(
    "interval",
    seconds=settings.film_works_run_interval,
    next_run_time=datetime.now(UTC) + timedelta(seconds=2),
)
def check_for_updated_film_works() -> None:
    logger.info("Checking for updated film works")
    with get_etl() as etl:
        etl.synchronize_film_work_updates()
