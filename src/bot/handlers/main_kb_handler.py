from datetime import datetime
from typing import Any

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.bot.keyboards.calendar_kb import get_multi_calendar
from src.enums import MainMenuIcons

main_callback_router = Router()


@main_callback_router.message(F.text == f"{MainMenuIcons.CALENDAR} Календар")
async def show_calendar(message: types.Message, state: FSMContext) -> None:
    now: datetime = datetime.now()
    current_year: int = now.year
    current_month: int = now.month

    data: dict[str, Any] = {
        "current_year": current_year,
        "current_month": current_month,
        "selected_days": [],
    }

    await state.update_data(data=data)

    await message.answer(
        "Оберіть дату:",
        reply_markup=get_multi_calendar(current_year, current_month),
    )


@main_callback_router.message(F.text == f"{MainMenuIcons.ADD_TASK} Додавання завдання")
async def add_task(message: types.Message) -> None:
    await show_message(message, "Додавання завдання")


@main_callback_router.message(F.text == f"{MainMenuIcons.REMINDER} Нагадування")
async def show_reminder(message: types.Message) -> None:
    await show_message(message, "Нагадування")


@main_callback_router.message(F.text == f"{MainMenuIcons.SHEDULE} Розклад дня")
async def show_schedule(message: types.Message) -> None:
    await show_message(message, "Розклад дня")


async def show_message(message: types.Message, text: str) -> None:
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
