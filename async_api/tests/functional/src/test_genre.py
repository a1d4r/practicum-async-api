from uuid import uuid4

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from httpx import AsyncClient

from models.genre import Genre
from tests.functional.settings import settings
from tests.functional.utils.factories import GenreFactory


async def insert_genres(es_client: AsyncElasticsearch, genres: list[Genre]):
    documents = [
        {
            "_index": settings.es_genres_index,
            "_id": str(genre.id),
            "_source": genre.model_dump(mode="json"),
        }
        for genre in genres
    ]
    await async_bulk(es_client, documents, refresh="wait_for")


async def test_list_genres(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    genres: list[Genre] = GenreFactory.batch(15)
    await insert_genres(es_client, genres)

    # Act
    response = await test_client.get("/v1/genres/", params={"page_number": 1, "page_size": 10})

    # Assert
    assert response.status_code == 200

    response_genres = response.json()
    assert len(response_genres) == 10
    assert {response_genre["uuid"] for response_genre in response_genres} <= {
        str(genre.id) for genre in genres
    }

    some_genre = response_genres[0]
    genre_in_es = next((genre for genre in genres if str(genre.id) == some_genre["uuid"]), None)
    assert genre_in_es is not None
    assert some_genre["name"] == genre_in_es.name


async def test_get_genre_details(test_client: AsyncClient, es_client: AsyncElasticsearch):
    genre: Genre = GenreFactory.build()
    await insert_genres(es_client, [genre])

    response = await test_client.get(f"/v1/genres/{genre.id}")

    assert response.status_code == 200
    response_genre = response.json()
    assert response_genre["name"] == genre.name
    assert response_genre["description"] == genre.description


async def test_get_non_existent_genre_details(test_client: AsyncClient):
    # Arrange
    non_existent_genre_id = uuid4()

    # Act
    response = await test_client.get(f"/v1/genres/{non_existent_genre_id}")

    # Assert
    assert response.status_code == 404


async def test_get_genre_details_from_cache(
    test_client: AsyncClient,
    es_client: AsyncElasticsearch,
):
    # Arrange
    genre: Genre = GenreFactory.build()
    await insert_genres(es_client, [genre])

    # Act
    await test_client.get(f"/v1/genres/{genre.id}")
    await es_client.delete(index=settings.es_genres_index, id=str(genre.id), refresh="wait_for")
    response = await test_client.get(f"/v1/genres/{genre.id}")

    # Assert
    assert response.status_code == 200
    response_genre = response.json()
    assert response_genre["name"] == genre.name
