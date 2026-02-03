from aiogram.types import ReplyKeyboardMarkup

from src.bot.keyboards.main_kd import get_main_keyboard
from src.enums.main_menu_icons import MainMenuIcons


def test_content_in_main_kb() -> None:
    main_keyboard_markup = get_main_keyboard()

    assert isinstance(main_keyboard_markup, ReplyKeyboardMarkup)

    main_keyboard = main_keyboard_markup.keyboard

    for index, text in enumerate(get_main_buttons_info()):
        assert main_keyboard[index][0].text == text

    assert main_keyboard_markup.resize_keyboard is True
    assert main_keyboard_markup.input_field_placeholder == "Оберіть дію..."
    assert len(main_keyboard) == len(get_main_buttons_info())


def get_main_buttons_info() -> list[str]:
    return [
        f"{MainMenuIcons.CALENDAR} Календар",
        f"{MainMenuIcons.ADD_TASK} Додавання завдання",
        f"{MainMenuIcons.REMINDER} Нагадування",
        f"{MainMenuIcons.SHEDULE} Розклад дня",
    ]
