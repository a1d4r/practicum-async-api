from loguru import logger

from etl import dto, transformer
from etl.extractor import PostgresExtractor
from etl.loader import ElasticsearchLoader
from etl.settings import Settings
from etl.state import ETLState, StateManager


class ETL:
    """Класс, отвечающий за выполнение ETL-процесса.

    Предоставляет функции для синхронизации обновлений жанров, персон и
    фильмов из PostgreSQL в Elasticsearch.
    """

    def __init__(
        self,
        state_manager: StateManager[ETLState],
        extractor: PostgresExtractor,
        loader: ElasticsearchLoader,
        settings: Settings,
    ) -> None:
        self.state_manager = state_manager
        self.extractor = extractor
        self.loader = loader
        self.settings = settings

    def synchronize_person_updates(self) -> None:
        """Синхронизирует обновления персон."""
        with self.state_manager.acquire_state() as state:
            logger.info("Retrieving persons updated since {}", state.persons_modified_cursor)
            persons = self.extractor.fetch_updated_persons(
                state.persons_modified_cursor,
                count=self.settings.persons_per_run,
            )

            if not persons:
                logger.info("No persons were updated since {}", state.persons_modified_cursor)
                return

            logger.debug("Persons IDs: {}", persons)
            logger.info(
                "Retrieved {} persons updated since {}",
                len(persons),
                state.persons_modified_cursor,
            )

            self._update_persons_in_elasticsearch(persons)

            for film_works in self.extractor.fetch_film_works_with_persons_in_batches(persons):
                self._update_film_works_in_elasticsearch(film_works)

            state.persons_modified_cursor = persons[-1].modified
            self.state_manager.save_state(state)

        logger.info("Moved persons cursor to {}", state.persons_modified_cursor)

    def synchronize_genre_updates(self) -> None:
        """Синхронизирует обновления жанров."""
        with self.state_manager.acquire_state() as state:
            logger.info("Retrieving genres updated since {}", state.genres_modified_cursor)
            genres = self.extractor.fetch_updated_genres(
                state.genres_modified_cursor,
                count=self.settings.genres_per_run,
            )
            if not genres:
                logger.info("No genres were updated since {}", state.genres_modified_cursor)
                return

            self._update_genres_in_elasticsearch(genres)

            for film_works in self.extractor.fetch_film_works_with_genres_in_batches(genres):
                self._update_film_works_in_elasticsearch(film_works)

            state.genres_modified_cursor = genres[-1].modified
            self.state_manager.save_state(state)

        logger.info("Moved genres cursor to {}", state.genres_modified_cursor)

    def synchronize_film_work_updates(self) -> None:
        """Синхронизирует обновления фильмов."""
        with self.state_manager.acquire_state() as state:
            logger.info("Retrieving film works updated since {}", state.film_works_modified_cursor)
            film_works = self.extractor.fetch_updated_film_works(
                state.film_works_modified_cursor,
                count=self.settings.film_works_per_run,
            )
            if not film_works:
                logger.info("No film works were updated since {}", state.film_works_modified_cursor)
                return
            logger.debug("Film works IDs: {}", film_works)
            logger.info(
                "Retrieved {} film works updated since {}",
                len(film_works),
                state.film_works_modified_cursor,
            )

            self._update_film_works_in_elasticsearch(film_works)

            state.film_works_modified_cursor = film_works[-1].modified
            self.state_manager.save_state(state)

        logger.info("Moved film works cursor to {}", state.film_works_modified_cursor)

    def _update_genres_in_elasticsearch(self, genres: list[dto.GenreIdModified]) -> None:
        """Обновляет данные о жанрах в Elasticsearch."""
        logger.info("Retrieved {} genres", len(genres))

        genres_info = self.extractor.fetch_genres_info(genres)
        genres_elasticsearch_records = transformer.build_genres_elasticsearch_records(
            genres_info,
        )
        self.loader.load_genres_records(genres_elasticsearch_records)

    def _update_persons_in_elasticsearch(self, persons: list[dto.PersonIdModified]) -> None:
        """Обновляет данные о персонах в Elasticsearch."""
        logger.info("Retrieved {} persons", len(persons))

        persons_info = self.extractor.fetch_persons_info(persons)
        persons_film_works = self.extractor.fetch_persons_film_works(persons)

        persons_elasticsearch_records = transformer.build_persons_elasticsearch_records(
            persons_info,
            persons_film_works,
        )
        self.loader.load_persons_records(persons_elasticsearch_records)

    def _update_film_works_in_elasticsearch(self, film_works: list[dto.FilmWorkIdModified]) -> None:
        """Обновляет данные о фильмах в Elasticsearch."""
        logger.info("Retrieved {} film works with updated persons", len(film_works))

        film_works_info = self.extractor.fetch_film_works_info(film_works)
        film_works_genres = self.extractor.fetch_film_works_genres(film_works)
        film_works_persons = self.extractor.fetch_film_works_persons(film_works)

        film_works_elasticsearch_records = transformer.build_film_works_elasticsearch_records(
            film_works_info=film_works_info,
            film_works_genres=film_works_genres,
            film_works_persons=film_works_persons,
        )
        self.loader.load_film_works_records(film_works_elasticsearch_records)
