import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_multi_calendar(
    year: int = None, month: int = None, selected_dates: list = None
):
    now = datetime.now()
    year: int = year or now.year
    month: int = month or now.month
    selected_dates = selected_dates or []
    builder = InlineKeyboardBuilder()

    month_names: list[str] = [
        "Січень",
        "Лютий",
        "Березень",
        "Квітень",
        "Травень",
        "Червень",
        "Липень",
        "Серпень",
        "Вересень",
        "Жовтень",
        "Листопад",
        "Грудень",
    ]

    days: list[str] = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]

    builder.add(
        InlineKeyboardButton(text=month_names[month], callback_data="month_callback")
    )
    builder.row(
        *[
            InlineKeyboardButton(text=day, callback_data=f"day_{i}")
            for i, day in enumerate(days)
        ]
    )

    for week in calendar.monthcalendar(year, month):
        row: list[InlineKeyboardButton] = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
            else:
                date = f"{day:02d}-{month:02d}-{year}"
                text = f"✅ {day}" if date in selected_dates else str(day)
                row.append(
                    InlineKeyboardButton(text=text, callback_data=f"date:{date}")
                )
        builder.row(*row)

    builder.row(
        InlineKeyboardButton(text="Підтвердити", callback_data="calendar_confirm")
    )

    return builder.as_markup()
