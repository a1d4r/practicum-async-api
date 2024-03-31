from uuid import uuid4

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from httpx import AsyncClient

from models.film import Film
from tests.functional.settings import settings
from tests.functional.utils.factories import FilmFactory, GenreIdNameFactory


async def insert_films(es_client: AsyncElasticsearch, films: list[Film]):
    documents = [
        {
            "_index": settings.es_films_index,
            "_id": str(film.id),
            "_source": film.model_dump(mode="json"),
        }
        for film in films
    ]
    await async_bulk(es_client, documents, refresh="wait_for")


async def test_list_films(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    films: list[Film] = FilmFactory.batch(15)
    await insert_films(es_client, films)

    # Act
    response = await test_client.get("/v1/films/", params={"page_number": 1, "page_size": 10})

    # Assert
    assert response.status_code == 200

    response_films = response.json()
    assert len(response_films) == 10
    assert {response_film["uuid"] for response_film in response_films} <= {
        str(film.id) for film in films
    }

    some_film = response_films[0]
    film_in_es = next((film for film in films if str(film.id) == some_film["uuid"]), None)
    assert film_in_es is not None
    assert some_film["title"] == film_in_es.title
    assert some_film["imdb_rating"] == film_in_es.imdb_rating


async def test_list_films_filter_by_genre(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    action_genre = GenreIdNameFactory.build(name="Action")
    comedy_genre = GenreIdNameFactory.build(name="Comedy")
    action_films: list[Film] = FilmFactory.batch(3, genres=[action_genre])
    comedy_films: list[Film] = FilmFactory.batch(2, genres=[comedy_genre])
    await insert_films(es_client, action_films + comedy_films)

    # Act
    response = await test_client.get("/v1/films/", params={"genre": "Comedy"})

    # Assert
    assert response.status_code == 200
    response_films = response.json()
    assert {response_film["uuid"] for response_film in response_films} == {
        str(film.id) for film in comedy_films
    }


async def test_get_film_details(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    film: Film = FilmFactory.build()
    await insert_films(es_client, [film])

    # Act
    response = await test_client.get(f"/v1/films/{film.id}")

    # Assert
    assert response.status_code == 200
    response_film = response.json()
    assert response_film["title"] == film.title
    assert response_film["imdb_rating"] == film.imdb_rating
    assert response_film["description"] == film.description
    assert response_film["genres"] == [
        {"uuid": str(genre.id), "name": genre.name} for genre in film.genres
    ]
    assert response_film["directors"] == [
        {"uuid": str(director.id), "name": director.name} for director in film.directors
    ]
    assert response_film["actors"] == [
        {"uuid": str(actor.id), "name": actor.name} for actor in film.actors
    ]
    assert response_film["writers"] == [
        {"uuid": str(writer.id), "name": writer.name} for writer in film.writers
    ]


async def test_get_non_existent_film_details(test_client: AsyncClient):
    # Arrange
    non_existent_film_id = uuid4()

    # Act
    response = await test_client.get(f"/v1/films/{non_existent_film_id}")

    # Assert
    assert response.status_code == 404


async def test_get_film_details_from_cache(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    film: Film = FilmFactory.build()
    await insert_films(es_client, [film])

    # Act
    await test_client.get(f"/v1/films/{film.id}")
    await es_client.delete(index=settings.es_films_index, id=str(film.id), refresh="wait_for")
    response = await test_client.get(f"/v1/films/{film.id}")

    # Assert
    assert response.status_code == 200
    response_film = response.json()
    assert response_film["title"] == film.title
    assert response_film["imdb_rating"] == film.imdb_rating
    assert response_film["description"] == film.description


async def test_search_films_by_name(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    film: Film = FilmFactory.build(title="Star Wars")
    await insert_films(es_client, [film])

    # Act
    response = await test_client.get("/v1/films/search", params={"query": "Star"})

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    found_film = response.json()[0]
    assert found_film["uuid"] == str(film.id)
    assert found_film["title"] == film.title
    assert found_film["imdb_rating"] == film.imdb_rating


async def test_search_films_not_found(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    film: Film = FilmFactory.build(title="Star Wars")
    await insert_films(es_client, [film])

    # Act
    response = await test_client.get("/v1/films/search", params={"query": "The Lord of the Rings"})

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 0
