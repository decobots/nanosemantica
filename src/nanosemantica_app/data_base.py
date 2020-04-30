import logging

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import NullPool
from .preparation.environment_variables import get_env

log = logging.getLogger()
Base = declarative_base()


class DataBase:
    session = None
    Session = None

    def __init__(self, url=None):
        # можно напрямую пердать url, например для тестирования
        url = url or get_env('DATABASE_URL')
        self.url = url
        self.engine = create_engine(url, echo=False, poolclass=NullPool)
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        log.debug(f"opened session to db {self.url}")

    def clean(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        log.debug(f"cleaned db")


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return self.name


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return self.name


class Component(Base):
    __tablename__ = "components"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer)
    items = relationship(Item)
    recipes = relationship(Recipe)

    def __repr__(self):
        return f'{self.recipe_id} {self.item_id} {self.quantity}'
