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
            genre=[genre.genre_name for genre in genres_by_film_work_id[film_work_info.id]],
            title=film_work_info.title,
            description=film_work_info.description,
            director=[
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
                dto.PersonElasticsearchRecord(id=fwp.person_id, name=fwp.person_full_name)
                for fwp in persons_by_film_work_id[film_work_info.id]
                if fwp.role == "actor"
            ],
            writers=[
                dto.PersonElasticsearchRecord(id=fwp.person_id, name=fwp.person_full_name)
                for fwp in persons_by_film_work_id[film_work_info.id]
                if fwp.role == "writer"
            ],
        )
        for film_work_info in film_works_info
    ]
