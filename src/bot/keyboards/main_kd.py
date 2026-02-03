from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.enums.main_menu_icons import MainMenuIcons


def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text=f"{MainMenuIcons.CALENDAR} Календар"),
        KeyboardButton(text=f"{MainMenuIcons.ADD_TASK} Додавання завдання"),
        KeyboardButton(text=f"{MainMenuIcons.REMINDER} Нагадування"),
        KeyboardButton(text=f"{MainMenuIcons.SHEDULE} Розклад дня"),
    )
    builder.adjust(1)

    return builder.as_markup(
        input_field_placeholder="Оберіть дію...", resize_keyboard=True
    )
