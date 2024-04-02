from uuid import uuid4

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from httpx import AsyncClient

from models.person import Person
from tests.functional.settings import settings
from tests.functional.utils.factories import PersonFactory


async def insert_persons(es_client: AsyncElasticsearch, persons: list[Person]):
    documents = [
        {
            "_index": settings.es_persons_index,
            "_id": str(person.id),
            "_source": person.model_dump(mode="json"),
        }
        for person in persons
    ]
    await async_bulk(es_client, documents, refresh="wait_for")


async def test_list_persons(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    persons: list[Person] = PersonFactory.batch(15)
    await insert_persons(es_client, persons)

    # Act
    response = await test_client.get(
        "/v1/persons/search",
        params={"page_number": 1, "page_size": 10},
    )

    # Assert
    assert response.status_code == 200

    response_persons = response.json()
    assert len(response_persons) == 10
    assert {response_person["uuid"] for response_person in response_persons} <= {
        str(person.id) for person in persons
    }

    some_person = response_persons[0]
    person_in_es = next(
        (person for person in persons if str(person.id) == some_person["uuid"]),
        None,
    )
    assert person_in_es is not None
    assert some_person["full_name"] == person_in_es.full_name
    assert some_person["films"] == [
        {"uuid": str(film.id), "roles": film.roles} for film in person_in_es.films
    ]


async def test_search_person_by_name(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    person = PersonFactory.build(full_name="John Cena")
    await insert_persons(es_client, [person])

    # Act
    response = await test_client.get(
        "/v1/persons/search",
        params={"query": "John"},
    )

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    response_person = response.json()
    first_person = response_person[0]

    assert first_person["films"] is not None
    assert first_person["films"] == [
        {"uuid": str(person.id), "roles": person.roles} for person in person.films
    ]


async def test_get_person_details(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    person: Person = PersonFactory.build()
    await insert_persons(es_client, [person])

    # Act
    response = await test_client.get(f"/v1/persons/{person.id}")

    # Assert
    assert response.status_code == 200
    response_person = response.json()
    assert response_person["full_name"] == person.full_name
    assert response_person["films"] == [
        {"uuid": str(film.id), "roles": film.roles} for film in person.films
    ]


async def test_get_non_existent_person_details(test_client: AsyncClient):
    # Arrange
    non_existent_person_id = uuid4()

    # Act
    response = await test_client.get(f"/v1/persons/{non_existent_person_id}")

    # Assert
    assert response.status_code == 404


async def test_get_person_details_from_cache(
    test_client: AsyncClient,
    es_client: AsyncElasticsearch,
):
    # Arrange
    person: Person = PersonFactory.build()
    await insert_persons(es_client, [person])

    # Act
    await test_client.get(f"/v1/persons/{person.id}")
    await es_client.delete(index=settings.es_persons_index, id=str(person.id), refresh="wait_for")
    response = await test_client.get(f"/v1/persons/{person.id}")

    # Assert
    assert response.status_code == 200
    response_person = response.json()
    assert response_person["full_name"] == person.full_name
    assert response_person["films"] == [
        {"uuid": str(film.id), "roles": film.roles} for film in person.films
    ]


async def test_get_films_by_person(test_client: AsyncClient, es_client: AsyncElasticsearch):
    # Arrange
    person: Person = PersonFactory.build()

    await insert_persons(es_client, [person])

    # Act
    response = await test_client.get(
        f"/v1/persons/{person.id}/films",
    )

    # Assert
    assert response.status_code == 200

    response_persons = response.json()
    some_film = response_persons[0]
    assert some_film["imdb_rating"] == person.films[0].imdb_rating
    assert some_film["roles"] == person.films[0].roles
    assert some_film["title"] == person.films[0].title
