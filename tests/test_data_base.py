import os

import pytest
from preparation.data_base import DataBase, Component, Recipe, Item

src_to_db = os.path.join(os.path.dirname(__file__), 'test.db')  # pragma: no cover


def test_db_init():
    DataBase()
    with open(src_to_db):
        pass
    os.remove(src_to_db)
    with pytest.raises(FileNotFoundError):
        open(src_to_db)


def test_db_clean(empty_database):
    test_recipe = Recipe(name='test recipe')
    test_item = Item(name='test item')
    empty_database.session.add(test_recipe)
    empty_database.session.add(test_item)
    empty_database.session.commit()
    test_componenet = Component(recipe_id=test_recipe.id, item_id=test_item.id, quantity=100)
    empty_database.session.add(test_componenet)
    empty_database.session.commit()
    empty_database.clean()
    recipes = empty_database.session.query(Recipe).all()
    items = empty_database.session.query(Item).all()
    components = empty_database.session.query(Component).all()
    assert len(recipes) == 0
    assert len(items) == 0
    assert len(components) == 0


def test_clean_empty_db(empty_database):
    empty_database.clean()  # test that there no errors when database clean


def test_recipes(empty_database):
    name = "test"
    test_recipe = Recipe(name=name)
    empty_database.session.add(test_recipe)
    empty_database.session.commit()

    all_recipes = empty_database.session.query(Recipe).all()
    assert len(all_recipes) == 1
    assert all_recipes[0].name == name


def test_items(empty_database):
    name = "test"
    test_item = Item(name=name)
    empty_database.session.add(test_item)
    empty_database.session.commit()

    all_items = empty_database.session.query(Item).all()
    assert len(all_items) == 1
    assert all_items[0].name == name


def test_lines(empty_database):
    quantity = 100
    test_recipe = Recipe(name='test recipe')
    test_item = Item(name='test item')
    empty_database.session.add(test_recipe)
    empty_database.session.add(test_item)
    empty_database.session.commit()
    test_componenet = Component(recipe_id=test_recipe.id, item_id=test_item.id, quantity=quantity)
    empty_database.session.add(test_componenet)
    empty_database.session.commit()

    all_Components = empty_database.session.query(Component).all()
    assert len(all_Components) == 1
    assert all_Components[0].recipe_id == test_recipe.id
    assert all_Components[0].item_id == test_item.id
    assert all_Components[0].quantity == quantity
