from typing import TYPE_CHECKING

from collections import defaultdict

from etl import dto

if TYPE_CHECKING:
    from uuid import UUID


def build_film_works_elasticsearch_records(
    film_works_info: list[dto.FilmWorkInfo],
    film_works_genres: list[dto.FilmWorkGenreRecord],
    film_works_persons: list[dto.FilmWorkPersonRecord],
) -> list[dto.FilmWorkElasticsearchRecord]:
    """Преобразовывает данные о фильмах в формат, пригодный для индекса в Elasticsearch."""
    genres_by_film_work_id: dict[UUID, list[dto.FilmWorkGenreRecord]] = defaultdict(list)
    for fwg in film_works_genres:
        genres_by_film_work_id[fwg.film_work_id].append(fwg)
    persons_by_film_work_id: dict[UUID, list[dto.FilmWorkPersonRecord]] = defaultdict(list)
    for fwp in film_works_persons:
        persons_by_film_work_id[fwp.film_work_id].append(fwp)
    return [
        dto.FilmWorkElasticsearchRecord(
            id=film_work_info.id,
            imdb_rating=film_work_info.rating,
            genres=[
                dto.GenreMinimalElasticsearchRecord(id=genre.genre_id, name=genre.genre_name)
                for genre in genres_by_film_work_id[film_work_info.id]
            ],
            title=film_work_info.title,
            description=film_work_info.description,
            directors_names=[
                fwp.person_full_name
                for fwp in persons_by_film_work_id[film_work_info.id]
                if fwp.role == "director"
            ],
            actors_names=[
                fwp.person_full_name
                for fwp in persons_by_film_work_id[film_work_info.id]
                if fwp.role == "actor"
            ],
            writers_names=[
                fwp.person_full_name
                for fwp in persons_by_film_work_id[film_work_info.id]
                if fwp.role == "writer"
            ],
            actors=[
                dto.PersonMinimalElasticsearchRecord(id=fwp.person_id, name=fwp.person_full_name)
                for fwp in persons_by_film_work_id[film_work_info.id]
                if fwp.role == "actor"
            ],
            writers=[
                dto.PersonMinimalElasticsearchRecord(id=fwp.person_id, name=fwp.person_full_name)
                for fwp in persons_by_film_work_id[film_work_info.id]
                if fwp.role == "writer"
            ],
            directors=[
                dto.PersonMinimalElasticsearchRecord(id=fwp.person_id, name=fwp.person_full_name)
                for fwp in persons_by_film_work_id[film_work_info.id]
                if fwp.role == "director"
            ],
        )
        for film_work_info in film_works_info
    ]


def build_genres_elasticsearch_records(
    genres_info: list[dto.GenreInfo],
) -> list[dto.GenreElasticsearchRecord]:
    """Преобразовывает данные о жанрах в формат, пригодный для индекса в Elasticsearch."""
    return [
        dto.GenreElasticsearchRecord(
            id=genre_info.id,
            name=genre_info.name,
            description=genre_info.description,
        )
        for genre_info in genres_info
    ]


def build_persons_elasticsearch_records(
    persons_info: list[dto.PersonInfo],
    persons_film_works: list[dto.PersonFilmWorkRecord],
) -> list[dto.PersonElasticsearchRecord]:
    """Преобразовывает данные о персонах в формат, пригодный для индекса в Elasticsearch."""
    films_by_person_id: dict[UUID, list[dto.PersonFilmWorkRecord]] = defaultdict(list)
    for pfw in persons_film_works:
        films_by_person_id[pfw.person_id].append(pfw)
    return [
        dto.PersonElasticsearchRecord(
            id=person_info.id,
            full_name=person_info.full_name,
            films=[
                dto.PersonFilmWorkElasticsearchRecord(
                    id=film.film_work_id,
                    title=film.title,
                    imdb_rating=film.rating,
                    roles=film.roles,
                )
                for film in films_by_person_id[person_info.id]
            ],
        )
        for person_info in persons_info
    ]
