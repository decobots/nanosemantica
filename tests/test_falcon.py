import pytest
from falcon import testing

from nanosemantica_app.falcon_app.app import create


@pytest.fixture()
def client(populated_database):
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    return testing.TestClient(create(populated_database.engine.url))


def test_post_message(client):
    json = {
        "мясо": 500,
        "огурец": 5,
        "картофель": 5
    }
    result = client.simulate_post('/', json=json)
    assert result.json == ['Салат «Русский»', 'Салат «Ленинградский»']
    assert result.status_code == 200


def test_post_message_empty_json(client):
    json = {}
    result = client.simulate_post('/', json=json)
    assert result.text == 'please add json with products, for example: {"мяcо":500}'
    assert result.status_code == 400


def test_post_message_no_json(client):
    result = client.simulate_post('/')
    assert result.text == 'please add json with products, for example: {"мяcо":500}'
    assert result.status_code == 400


def test_post_message_not_existing_product(client):
    json = {
        "черешня": 500,
    }
    result = client.simulate_post('/', json=json)
    assert result.json == []
    assert result.status_code == 200
