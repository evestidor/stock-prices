from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.domain import Price


class Storage(ABC):

    @abstractmethod
    def list(self) -> List[Price]:
        pass

    @abstractmethod
    def save(self, *prices: List[Price]) -> List[Price]:
        pass


class DBStorage(Storage):

    def __init__(self):
        self._engine = None
        self.init()

    def init(self):
        if self._engine is None:
            self._engine = create_engine('sqlite:///:memory:', echo=True)
            base = declarative_base()
            self._table = self._declare_table(base)
            base.metadata.create_all(self._engine)

    def save(self, *prices: List[Price]):
        session = sessionmaker(bind=self._engine)
        session.add_all(self._domain_to_table(*prices))

    def list(self) -> List[Price]:
        session = sessionmaker(bind=self._engine)
        result = session.query(self._table).all()
        return self._table_to_domain(result)

    def _declare_table(self, base):
        class Price(base):
            __tablename__ = 'prices'
            id = Column(Integer, primary_key=True)
            symbol = Column(String)
            amount = Column(String)
            created = Column(String)

        return Price

    def _domain_to_table(self, *prices: List[Price]):
        return [self._table(**vars(price)) for price in prices]

    def _table_to_domain(self, *instances) -> List[Price]:
        return [Price(**vars(instance)) for instance in instances]
