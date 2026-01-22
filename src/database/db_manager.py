import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_PATH
from src.database.models import Base


class DBManager:
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def init_db(self):
        db_dir = os.path.dirname(DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.SessionLocal()


db_manager = DBManager()
