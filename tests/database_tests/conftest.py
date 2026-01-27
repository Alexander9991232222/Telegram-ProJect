import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.db_manager import DBManager
from src.database.models import Base


@pytest.fixture
def temp_db() -> DBManager:
    manager = DBManager()
    manager.engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(manager.engine)

    manager.SessionLocal = sessionmaker(bind=manager.engine)
    return manager
