import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import settings
from src.database.models import Base


class DBManager:
    def __init__(self) -> None:
        self.engine = create_engine(f"sqlite:///{settings.db_path}", echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def init_db(self) -> None:
        db_dir = os.path.dirname(settings.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()


db_manager = DBManager()
