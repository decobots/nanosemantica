import json
import logging
from typing import Optional

import falcon
from falcon import request as FalconRequest, response as FalconResponse
from falcon_app.HandleCORS import HandleCORS
from logger import init_logging
from data_base import DataBase, Item, Component


class IvansHelper(object):
    def __init__(self, url: str = None):
        init_logging("log.log")
        self.log = logging.getLogger()
        self.db = DataBase(url)

    def on_post(self, req: FalconRequest, resp: FalconResponse):
        session = self.db.Session()
        try:
            freezer = req.media
            if freezer:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps([str(r) for r in choose_recipes(session, freezer)])
            else:
                self.log.debug(f"invalid request, freezer = {freezer}")
                resp.status = falcon.HTTP_400
                resp.body = 'please add json with products, for example: {"мяcо":500}'
        finally:
            session.close()


def choose_recipes(session, freezer):
    # что бы не делать перебор всех рецептов сначала найдем рецепты которые могут подходить,
    # на основании количества ингредиентов.
    good_recipes = []
    for name, quantity in freezer.items():
        item = session.query(Item).filter(Item.name == name).one_or_none()
        if item:
            recipes_for_item = session.query(Component).filter(Component.item_id == item.id,
                                                               Component.quantity <= quantity).all()
            good_recipes.extend([r.recipe_id for r in recipes_for_item])
        else:
            print(f"item {name} from freezer aren't found in database")
    correct = []

    for recipe_id in set(good_recipes):
        components_for_recipe = session.query(Component).filter(Component.recipe_id == recipe_id).all()
        index = 0
        for component in components_for_recipe:
            if component.quantity > freezer.get(str(component.items), 0):
                break
            else:
                index += 1
            if len(components_for_recipe) == index:
                correct.append(component.recipes)
    return correct


def create(url: Optional[str] = None) -> falcon.API:
    # можно напрямую пердать url, например для тестирования
    api = falcon.API(middleware=[HandleCORS()])
    helper = IvansHelper(url)
    api.add_route('/', helper)
    return api


app = create()
