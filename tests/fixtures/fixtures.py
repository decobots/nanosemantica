import os

import pytest
from nanosemantica_app.data_base import DataBase
from nanosemantica_app.preparation.preparation import process_cook_book

src_to_test_json = os.path.join(os.path.dirname(__file__), 'test_data', 'test.json')

src_to_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test.db')  # pragma: no cover


@pytest.fixture
def empty_database():
    if os.path.exists(src_to_db):
        os.remove(src_to_db)
    test_db = DataBase()
    yield test_db
    test_db.session.close()


@pytest.fixture
def populated_database(empty_database):
    test_db = empty_database
    src_to_test_json = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data", "test.json")
    process_cook_book(session=empty_database.session, src=src_to_test_json)
    yield test_db


@pytest.fixture
def global_variable():
    key = "TEST_VARIABLE"
    value = "TEST_VALUE"
    os.environ[key] = value
    yield key, value
    os.environ.pop(key)