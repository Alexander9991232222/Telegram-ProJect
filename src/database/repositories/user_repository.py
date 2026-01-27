from src.database.models.user import User
from src.database.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    @property
    def model(self) -> type[User]:
        return User

    pass
