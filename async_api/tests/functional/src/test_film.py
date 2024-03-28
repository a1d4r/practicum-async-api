import pytest


@pytest.mark.usefixtures("_create_indexes")
def test_dummy(es_client):
    assert True
