from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text="📅 Календар"),
        KeyboardButton(text="➕ Додавання завдання"),
        KeyboardButton(text="🔔 Нагадування"),
        KeyboardButton(text="📋 Розклад дня"),
    )
    builder.adjust(1)

    return builder.as_markup(
        input_field_placeholder="Оберіть дію...", resize_keyboard=True
    )
