from aiogram import F, Router, types
from aiogram.types import ReplyKeyboardRemove

main_callback_router = Router()


@main_callback_router.message(F.text == "📅 Календар")
async def show_calendar(message: types.Message):
    await show_message(message, "Календар")


@main_callback_router.message(F.text == "➕ Додавання завдання")
async def add_task(message: types.Message):
    await show_message(message, "Додавання завдання")


@main_callback_router.message(F.text == "🔔 Нагадування")
async def show_reminder(message: types.Message):
    await show_message(message, "Нагадування")


@main_callback_router.message(F.text == "📋 Розклад дня")
async def show_schedule(message: types.Message):
    await show_message(message, "Розклад дня")


async def show_message(message: types.Message, text: str):
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
