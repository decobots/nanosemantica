import os

import pytest
from preparation.data_base import Component, Recipe, Item
from preparation.preparation import process_cook_book


def test_process_cook_book(empty_database):
    src_to_test_json = os.path.join(os.path.dirname(__file__), "test_data", "test.json")

    process_cook_book(session=empty_database.session, src=src_to_test_json)
    all_recipes = empty_database.session.query(Recipe).all()
    all_items = empty_database.session.query(Item).all()
    all_components = empty_database.session.query(Component).all()
    assert len(all_recipes) == 3
    assert len(all_items) == 5
    assert len(all_components) == 7

    assert all_recipes[2].name == "Салат с рыбой и овощами"
    assert all_items[4].name == 'яйцо'
    assert all_components[6].recipe_id == 3
    assert all_components[6].item_id == 5
    assert all_components[6].quantity == 3


def test_process_cook_book_empty_json(empty_database):
    src_to_test_json = os.path.join(os.path.dirname(__file__), "test_data", "empty.json")
    with pytest.raises(ValueError):
        process_cook_book(session=empty_database.session, src=src_to_test_json)


def test_process_cook_book_empty_json2(empty_database):
    src_to_test_json = os.path.join(os.path.dirname(__file__), "test_data", "empty2.json")

    process_cook_book(session=empty_database.session, src=src_to_test_json)
    all_recipes = empty_database.session.query(Recipe).all()
    all_items = empty_database.session.query(Item).all()
    all_components = empty_database.session.query(Component).all()
    assert len(all_recipes) == 0
    assert len(all_items) == 0
    assert len(all_components) == 0
