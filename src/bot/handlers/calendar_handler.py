import calendar
from typing import cast

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards.calendar_kb import get_multi_calendar

calendar_router = Router()


@calendar_router.callback_query(F.data.startswith("cal_day:"))
async def calendar_day_callback_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    if not callback.data or not isinstance(callback.message, Message):
        return

    selected_day_id: str = callback.data.split(":")[1]

    data = await state.get_data()
    selected_days: list[str] = data.get("selected_days", [])
    current_year: int = cast(int, data.get("current_year"))
    current_month: int = cast(int, data.get("current_month"))

    if selected_day_id in selected_days:
        selected_days.remove(selected_day_id)
    else:
        selected_days.append(selected_day_id)

    await state.update_data(selected_days=selected_days)

    await callback.message.edit_reply_markup(
        reply_markup=get_multi_calendar(current_year, current_month, selected_days),
    )

    await callback.answer()


@calendar_router.callback_query(
    F.data.startswith(("cal_days_in_month:", "cal_week_days:"))
)
async def calendar_mass_selection_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    if not callback.data or not isinstance(callback.message, Message):
        return

    prefix, payload = callback.data.split(":")
    parts = payload.split("-")

    idx, month, year = int(parts[0]), int(parts[1]), int(parts[2])

    data = await state.get_data()
    selected_days: list[str] = data.get("selected_days", [])
    month_calendar: list[list[int]] = calendar.monthcalendar(year, month)

    if prefix == "cal_days_in_month":
        target_days = [
            f"{d:02d}-{month:02d}-{year}"
            for week in month_calendar
            if (d := week[idx]) > 0
        ]
    else:
        target_days = [
            f"{d:02d}-{month:02d}-{year}" for d in month_calendar[idx] if d > 0
        ]

    updated_days = toggle_dates_list(selected_days, target_days)

    await state.update_data(selected_days=updated_days)
    await callback.message.edit_reply_markup(
        reply_markup=get_multi_calendar(year, month, updated_days)
    )
    await callback.answer()


def toggle_dates_list(
    current_selection: list[str], dates_to_toggle: list[str]
) -> list[str]:
    selection_set = set(current_selection)
    toggle_set = set(dates_to_toggle)

    if toggle_set.issubset(selection_set):
        return [d for d in current_selection if d not in toggle_set]
    else:
        for d_id in dates_to_toggle:
            if d_id not in selection_set:
                current_selection.append(d_id)
        return current_selection
