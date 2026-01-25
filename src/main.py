from sqlalchemy import select

from src.database import db_manager
from src.database.models import User


def main():
    print("Initializing database...")
    db_manager.init_db()
    print("Database initialized")

    with db_manager.get_session() as session:
        test_id = 77
        query = select(User).filter_by(id=test_id)
        user = session.execute(query).scalar_one_or_none()

        if user is None:
            user = User(
                id=test_id,
                chat_id=test_id,
                user_name=f"test_{test_id}",
                first_name=f"test_{test_id}",
            )
            session.add(user)
            session.commit()
            print(f"User with id {test_id} added")
        else:
            print(f"User with id {test_id} already exists")


if __name__ == "__main__":
    main()
