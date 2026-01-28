from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.services.calendar_generator import generate_calendar


def get_multi_calendar(
    year: int, month: int, selected_days: list[str] | None = None
) -> InlineKeyboardMarkup:
    calendar = generate_calendar(year, month, selected_days)
    builder = InlineKeyboardBuilder()

    for row in calendar:
        row_buttons = [
            InlineKeyboardButton(text=btn.text, callback_data=btn.callback_data)
            for btn in row
        ]
        builder.row(*row_buttons)

    return builder.as_markup()
