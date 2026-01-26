from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(ABC):
    @property
    @abstractmethod
    def model(self) -> type[T]:
        pass

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id) -> T:
        return self.session.get(self.model, id)

    def delete_by_id(self, id):
        record = self.get_by_id(id)
        self.session.delete(record)
        self.session.commit()

    def update_by_id(self, id, data):
        record = self.get_by_id(id)
        for key, value in data.items():
            setattr(record, key, value)
        self.session.commit()

    def create(self, data):
        record = self.model(**data)
        self.session.add(record)
        self.session.commit()

    def get_by_filters(self, *filters) -> list[T]:
        query = select(self.model).where(*filters)
        result = self.session.execute(query)
        return list(result.scalars().all())
