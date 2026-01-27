import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.bot.handlers import calendar_router, main_callback_router, start_router
from src.config import settings
from src.database import db_manager
from src.database.models.base import Base


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Initializing database")
    engine = db_manager.engine
    Base.metadata.create_all(engine)
    logging.info("Database initialized")

    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(main_callback_router)
    dp.include_router(calendar_router)
    dp["db_manager"] = db_manager

    logging.info("Starting bot")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped by user")
