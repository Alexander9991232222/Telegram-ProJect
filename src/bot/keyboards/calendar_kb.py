from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_multi_calendar(
    year: int, month: int, selected_dates: list[str]
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    return builder.as_markup()
