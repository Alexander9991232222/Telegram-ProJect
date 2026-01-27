from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from src.database.db_manager import DBManager


def test_init_db_create_tables(temp_db: DBManager) -> None:
    temp_db.init_db()
    inspector = inspect(temp_db.engine)
    existing_tables = inspector.get_table_names()

    assert "user" in existing_tables, "Table 'user' in not created"


def test_get_session_returns_valid_session(temp_db: DBManager) -> None:
    with temp_db.get_session() as session:
        assert isinstance(session, Session)

        query = "SELECT 1"
        result = session.execute(text(query)).scalar()

        assert result == 1
