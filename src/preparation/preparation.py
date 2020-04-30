import json
import logging
import os
from json import JSONDecodeError

from logger import init_logging
from data_base import DataBase, Recipe, Item, Component

log = logging.getLogger()


def process_cook_book(session, src):
    with open(src, encoding='utf-8') as f:
        try:
            data = json.load(f)
        except JSONDecodeError:
            raise ValueError('file does not contain JSON object')
        recipes = data.get('recipes', [])

    for recipe in recipes:
        r = Recipe(name=recipe['name'])
        session.add(r)
        session.commit()  # коммит потому что ниже потребуется id
        for component in recipe['components']:
            # проверяем добавлен ли продукт в бвз данных ранее, поскольку продукты повторяются этот вариант вероятнее
            # и проверяется первым.
            i = session.query(Item).filter(Item.name == component['item']).one_or_none()
            if not i:
                i = Item(name=component['item'])
                session.add(i)
                session.commit()  # коммит потому что ниже потребуется id

            c = Component(recipe_id=r.id, item_id=i.id, quantity=component['q'])
            session.add(c)
        session.commit()
    log.info(f'added {len(recipes)} recipes to cookbook')


if __name__ == '__main__':
    init_logging("log_preparation.log")
    db = DataBase()
    # считаю что при перезапуске скрипта старую информацию можно очистить, на одинаковом файле рецептов база заполнится одинаково
    db.clean()
    ss = db.session
    src = os.path.join(os.path.dirname(__file__), 'task.json')  # pragma: no cover
    process_cook_book(session=ss, src=src)
