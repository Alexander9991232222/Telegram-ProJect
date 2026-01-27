import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from src.database.db_manager import DBManager
from src.database.models import Base, User


def test_user_model_registration() -> None:
    assert "user" in Base.metadata.tables


def test_user_column_definition() -> None:
    mapper = inspect(User)
    columns = [column.key for column in mapper.attrs]

    assert "id" in columns
    assert "chat_id" in columns
    assert "user_name" in columns
    assert "first_name" in columns
    assert "created_at" in columns


def test_user_id_is_primary_key() -> None:
    mapper = inspect(User)
    assert mapper.primary_key[0].name == "id"


def test_create_user_missing_required_fields(temp_db: DBManager) -> None:
    temp_db.init_db()

    with temp_db.get_session() as session:
        incomplete_user = User(first_name="Test")
        session.add(incomplete_user)

        with pytest.raises(IntegrityError):
            session.commit()
