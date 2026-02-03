from aiogram.types import InlineKeyboardMarkup

from src.bot.keyboards.calendar_kb import get_multi_calendar
from src.services.calendar_generator import generate_calendar


def test_mapping_compliance_check_in_calendar(year_and_month: tuple[int, int]) -> None:
    year, month = year_and_month

    calendar = generate_calendar(year, month, [])
    inline_key_board_markup = get_multi_calendar(year, month, [])

    assert isinstance(inline_key_board_markup, InlineKeyboardMarkup)

    key_board = inline_key_board_markup.inline_keyboard

    for row, items in enumerate(calendar):
        for col, day in enumerate(items):
            assert key_board[row][col].text == day.text
            assert key_board[row][col].callback_data == day.callback_data
