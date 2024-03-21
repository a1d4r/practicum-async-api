from uuid import UUID

import pytest

from models.person import Person
from services.person import PersonService


@pytest.fixture()
async def person_service(elastic):
    return PersonService(elastic)


async def test_get_person_by_id(person_service: PersonService):
    # Arrange
    george_lucas_id = UUID("a5a8f573-3cee-4ccc-8a2b-91cb9f55250a")

    # Act
    person = await person_service.get_by_id(george_lucas_id)

    # Assert
    assert person is not None
    assert person.id == george_lucas_id
    assert person.full_name == "George Lucas"
    assert len(person.films) == 46
    assert person.films[0].id == UUID("516f91da-bd70-4351-ba6d-25e16b7713b7")
    assert person.films[0].roles == ["director", "writer"]


async def test_search_persons(person_service: PersonService):
    # Arrange
    page = 2
    size = 5

    # Act
    persons = await person_service.search(page=page, size=size)

    # Assert
    assert len(persons) == size
    assert all(isinstance(person, Person) for person in persons)


async def test_search_persons_with_query(person_service: PersonService):
    # Arrange
    query = "George Lucas"
    george_lucas_id = UUID("a5a8f573-3cee-4ccc-8a2b-91cb9f55250a")

    # Act
    persons = await person_service.search(query=query)

    # Assert
    person = persons[0]
    assert person.id == george_lucas_id
    assert person.full_name == "George Lucas"
    assert len(person.films) == 46
    assert person.films[0].id == UUID("516f91da-bd70-4351-ba6d-25e16b7713b7")
    assert person.films[0].roles == ["director", "writer"]
