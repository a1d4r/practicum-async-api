from collections.abc import Iterator
from datetime import datetime

import psycopg
import tenacity

from loguru import logger
from psycopg.rows import DictRow

from etl import dto
from etl.dto import FilmWorkIdModified
from etl.settings import settings

retry = tenacity.retry(
    before_sleep=tenacity.before_sleep_log(logger, "ERROR"),  # type: ignore[arg-type]
    after=tenacity.after_log(logger, "INFO"),  # type: ignore[arg-type]
    retry=tenacity.retry_if_exception_type(psycopg.OperationalError),
    wait=settings.retry_policy,
)


class PostgresExtractor:
    """Класс, отвечающий за извлечение данных из PostgreSQL."""

    def __init__(self, connection: psycopg.Connection[DictRow], batch_size: int = 1000) -> None:
        self._connection = connection
        self._batch_size = batch_size

    @retry
    def fetch_updated_persons(
        self,
        since_timestamp: datetime,
        count: int,
    ) -> list[dto.PersonIdModified]:
        """Получить список персон, обновленных после заданной даты."""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, modified
                FROM content.person
                WHERE modified > %(since)s
                ORDER BY modified
                LIMIT %(limit)s
                """,
                ({"since": since_timestamp, "limit": count}),
            )
            return [dto.PersonIdModified(**row) for row in cursor.fetchall()]

    @retry
    def fetch_updated_genres(
        self,
        since_timestamp: datetime,
        count: int,
    ) -> list[dto.GenreIdModified]:
        """Получить список жанров, обновленных после заданной даты."""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, modified
                FROM content.genre
                WHERE modified > %(since)s
                ORDER BY modified
                LIMIT %(limit)s
                """,
                ({"since": since_timestamp, "limit": count}),
            )
            return [dto.GenreIdModified(**row) for row in cursor.fetchall()]

    @retry
    def fetch_updated_film_works(
        self,
        since_timestamp: datetime,
        count: int,
    ) -> list[FilmWorkIdModified]:
        """Получить список кинопроизведений, обновленных после заданной даты."""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, modified
                FROM content.film_work
                WHERE modified > %(since)s
                ORDER BY modified
                LIMIT %(limit)s
                """,
                ({"since": since_timestamp, "limit": count}),
            )
            return [dto.FilmWorkIdModified(**row) for row in cursor.fetchall()]

    @retry
    def fetch_film_works_with_persons_in_batches(
        self,
        persons: list[dto.PersonIdModified],
    ) -> Iterator[list[dto.FilmWorkIdModified]]:
        """Генератор по спискам кинопроизведений,
        в создании которых участвовали заданные персоны.
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT fw.id, fw.modified
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                WHERE pfw.person_id = ANY(%(persons_ids)s)
                ORDER BY fw.modified
                """,
                ({"persons_ids": [person.id for person in persons]}),
            )
            for batch in iter(lambda: cursor.fetchmany(self._batch_size), []):
                yield [dto.FilmWorkIdModified(**row) for row in batch]

    @retry
    def fetch_film_works_with_genres_in_batches(
        self,
        genres: list[dto.GenreIdModified],
    ) -> Iterator[list[dto.FilmWorkIdModified]]:
        """Генератор по спискам кинопроизведений с заданными жанрами."""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT fw.id, fw.modified
                FROM content.film_work fw
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                WHERE gfw.genre_id = ANY(%(genres_ids)s)
                ORDER BY fw.modified
                """,
                ({"genres_ids": [genre.id for genre in genres]}),
            )
            for batch in iter(lambda: cursor.fetchmany(self._batch_size), []):
                yield [dto.FilmWorkIdModified(**row) for row in batch]

    @retry
    def fetch_genres_info(
        self,
        genres: list[dto.GenreIdModified],
    ) -> list[dto.GenreInfo]:
        """Получить информацию о заданных жанрах."""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    description,
                    created,
                    modified
                FROM content.genre
                WHERE id = ANY(%(genres_ids)s)
                """,
                ({"genres_ids": [genre.id for genre in genres]}),
            )
            return [dto.GenreInfo(**row) for row in cursor.fetchall()]

    @retry
    def fetch_persons_info(
        self,
        persons: list[dto.PersonIdModified],
    ) -> list[dto.PersonInfo]:
        """Получить информацию о заданных персонах."""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    full_name,
                    created,
                    modified
                FROM content.person
                WHERE id = ANY(%(persons_ids)s)
                """,
                ({"persons_ids": [person.id for person in persons]}),
            )
            return [dto.PersonInfo(**row) for row in cursor.fetchall()]

    @retry
    def fetch_film_works_info(
        self,
        film_works: list[dto.FilmWorkIdModified],
    ) -> list[dto.FilmWorkInfo]:
        """Получить информацию о заданных кинопроизведениях."""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    fw.id,
                    fw.title,
                    fw.description,
                    fw.creation_date,
                    fw.rating,
                    fw.type,
                    fw.created,
                    fw.modified
                FROM content.film_work fw
                WHERE fw.id = ANY(%(film_works_ids)s)
                """,
                ({"film_works_ids": [film_work.id for film_work in film_works]}),
            )
            return [dto.FilmWorkInfo(**row) for row in cursor.fetchall()]

    @retry
    def fetch_film_works_genres(
        self,
        film_works: list[dto.FilmWorkIdModified],
    ) -> list[dto.FilmWorkGenreRecord]:
        """Получить жанры заданных кинопроизведений."""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    gfw.film_work_id AS film_work_id,
                    gfw.genre_id AS genre_id,
                    g.name AS genre_name
                FROM content.film_work fw
                INNER JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                INNER JOIN content.genre g on gfw.genre_id = g.id
                WHERE fw.id = ANY(%(film_works_ids)s)
                """,
                ({"film_works_ids": [film_work.id for film_work in film_works]}),
            )
            return [dto.FilmWorkGenreRecord(**row) for row in cursor.fetchall()]

    @retry
    def fetch_film_works_persons(
        self,
        film_works: list[dto.FilmWorkIdModified],
    ) -> list[dto.FilmWorkPersonRecord]:
        """Получить информацию о персонах, которые участвовали
        в создании заданных кинопроизведений.
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    pfw.film_work_id AS film_work_id,
                    pfw.person_id AS person_id,
                    p.full_name AS person_full_name,
                    pfw.role AS role
                FROM content.film_work fw
                INNER JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                INNER JOIN content.person p on p.id = pfw.person_id
                WHERE fw.id = ANY(%(film_works_ids)s)
                """,
                ({"film_works_ids": [film_work.id for film_work in film_works]}),
            )
            return [dto.FilmWorkPersonRecord(**row) for row in cursor.fetchall()]

    @retry
    def fetch_persons_film_works(
        self,
        persons: list[dto.PersonIdModified],
    ) -> list[dto.PersonFilmWorkRecord]:
        """Получить кинопроизведения и роли, в которых участвовала заданная персона."""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    person_id,
                    film_work_id,
                    title,
                    rating,
                    array_agg(role) AS roles
                FROM content.person_film_work pfw
                LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
                WHERE person_id = ANY(%(persons_ids)s)
                GROUP BY (person_id, film_work_id, title, rating)
                """,
                ({"persons_ids": [person.id for person in persons]}),
            )
            return [dto.PersonFilmWorkRecord(**row) for row in cursor.fetchall()]
