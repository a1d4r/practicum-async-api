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
    assert some_person["films"] == person_in_es.films


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
    assert response_person["films"] == person.films
