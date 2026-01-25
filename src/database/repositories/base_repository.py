from abc import ABC, abstractmethod
from typing import TypeVar

from pytest import Session
from sqlalchemy import select

from src.database.models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(ABC):
    def __init__(self, model: type[T], session: Session):
        self.model = (model,)
        self.session = session

    @abstractmethod
    def get_by_id(self, id) -> T:
        return self.session.get(self.model, id)

    @abstractmethod
    def delete_by_id(self, id):
        record = self.get_by_id(id)
        self.session.delete(record)
        self.session.commit()

    @abstractmethod
    def update_by_id(self, id, data):
        record = self.get_by_id(id)
        for key, value in data.items():
            setattr(record, key, value)
        self.session.commit()

    @abstractmethod
    def create(self, data):
        record = self.model(**data)
        self.session.add(record)
        self.session.commit()

    @abstractmethod
    def get_by_filters(self, *filters) -> list[T]:
        query = select(self.modle).where(*filters)
        result = self.session.execute(query)
        return list(result.scalars().all())
