from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast

from sqlalchemy import ColumnElement, select
from sqlalchemy.orm import Session

from src.database.models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T], ABC):
    @property
    @abstractmethod
    def model(self) -> type[T]:
        pass

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: int) -> T | None:
        return cast(T | None, self.session.get(self.model, id))

    def delete_by_id(self, id: int) -> None:
        record = self.get_by_id(id)
        if record:
            self.session.delete(record)
            self.session.commit()

    def update_by_id(self, id: int, data: dict[str, Any]) -> None:
        record = self.get_by_id(id)
        if record:
            for key, value in data.items():
                setattr(record, key, value)
            self.session.commit()

    def create(self, data: dict[str, Any]) -> None:
        record = self.model(**data)
        self.session.add(record)
        self.session.commit()

    def get_by_filters(self, *filters: ColumnElement[bool]) -> list[T]:
        query = select(self.model).where(*filters)
        result = self.session.execute(query)
        return list(result.scalars().all())
