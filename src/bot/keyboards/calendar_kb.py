import calendar
from datetime import datetime
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_multi_calendar(year: int = None, month: int = None, selected_dates: list = None):
    now = datetime.now()
    year, month = year or now.year, month or now.month
    selected_dates = selected_dates or []

    builder = InlineKeyboardBuilder()

    month_names = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", 
                   "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]
    builder.row(InlineKeyboardButton(text=f"{month_names[month-1]} {year}", callback_data="ignore"))

    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    builder.row(*[InlineKeyboardButton(text=d, callback_data="ignore") for d in days])

    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                is_selected = "✅ " if date_str in selected_dates else ""
                row.append(InlineKeyboardButton(
                    text=f"{is_selected}{day}", 
                    callback_data=f"mcal_date:{date_str}"
                ))
        builder.row(*row)

    builder.row(InlineKeyboardButton(text="✅ Підтвердити вибір", callback_data="mcal_confirm"))
    
    return builder.as_markup()