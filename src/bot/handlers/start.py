from aiogram import Router, types
from aiogram.filters import CommandStart

from src.bot.keyboards.main_kd import get_main_keyboard
from src.database.db_manager import DBManager
from src.database.repositories.user_repository import UserRepository

start_router = Router()


@start_router.message(CommandStart())
async def start(message: types.Message, db_manager: DBManager) -> None:
    if message.from_user is None:
        return

    with db_manager.get_session() as session:
        repo = UserRepository(session)
        user = repo.get_by_id(message.from_user.id)
        if user is None:
            repo.create(
                {
                    "id": message.from_user.id,
                    "user_name": message.from_user.username,
                    "first_name": message.from_user.first_name,
                    "chat_id": message.chat.id,
                }
            )

        await message.answer(
            f"Hello, {message.from_user.first_name}", reply_markup=get_main_keyboard()
        )
