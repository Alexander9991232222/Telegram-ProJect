from typing import Any

import pytest
from sqlalchemy import or_

from src.database.db_manager import DBManager
from src.database.models import User
from src.database.repositories.user_repository import UserRepository


@pytest.fixture
def user_data() -> dict[str, Any]:
    return {
        "id": 32,
        "first_name": "John",
        "user_name": "Test",
        "chat_id": 123,
    }


@pytest.fixture
def persisted_user(temp_db: DBManager, user_data: dict[str, Any]) -> dict[str, Any]:
    with temp_db.get_session() as session:
        repo = UserRepository(session)
        repo.create(user_data)
        session.commit()
        return user_data


def test_user_repository_create(temp_db: DBManager, user_data: dict[str, Any]) -> None:
    with temp_db.get_session() as session:
        repo = UserRepository(session)

        repo.create(user_data)

        user = repo.get_by_id(user_data["id"])

        assert user is not None, "User should be found in database"
        assert user.id == user_data["id"]
        assert user.first_name == user_data["first_name"]
        assert user.user_name == user_data["user_name"]
        assert user.chat_id == user_data["chat_id"]


def test_user_repository_update(
    temp_db: DBManager, persisted_user: dict[str, Any]
) -> None:
    with temp_db.get_session() as session:
        repo = UserRepository(session)
        update_data = {"first_name": "Alex", "user_name": "Test_123"}

        repo.update_by_id(persisted_user["id"], update_data)

        user = repo.get_by_id(persisted_user["id"])

        assert user is not None, "User should be found in database"
        assert user.id == persisted_user["id"]
        assert user.first_name == update_data["first_name"]
        assert user.user_name == update_data["user_name"]
        assert user.chat_id == persisted_user["chat_id"]


def test_user_repository_delete(
    temp_db: DBManager, persisted_user: dict[str, Any]
) -> None:
    with temp_db.get_session() as session:
        repo = UserRepository(session)
        repo.delete_by_id(persisted_user["id"])

        user = repo.get_by_id(persisted_user["id"])

        assert user is None


def test_user_repository_get_by_filters(temp_db: DBManager) -> None:
    with temp_db.get_session() as session:
        repo = UserRepository(session)

        repo.create(
            {"id": 32, "first_name": "John", "user_name": "Test_2", "chat_id": 123}
        )
        repo.create(
            {"id": 33, "first_name": "Alex", "user_name": "Test_2", "chat_id": 123}
        )

        users: list[User] = repo.get_by_filters(
            or_(User.first_name == "Alex", User.user_name == "Test_2")
        )

        assert len(users) == 2
