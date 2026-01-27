from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.bot.keyboards.calendar_kb import get_multi_calendar

calendar_router = Router()


@calendar_router.callback_query(F.data.startswith("date:"))
async def process_multi_select(callback: types.CallbackQuery, state: FSMContext):
    selected_date: str = callback.data.split(":")[1]
    data = await state.get_data()
    selected_dates: list[str] = data.get("selected_dates", [])

    if selected_date in selected_dates:
        selected_dates.remove(selected_date)
    else:
        selected_dates.append(selected_date)

    await state.update_data(selected_dates=selected_dates)

    await callback.message.edit_reply_markup(
        reply_markup=get_multi_calendar(selected_dates=selected_dates)
    )
    await callback.answer()


@calendar_router.callback_query(F.data == "calendar_confirm")
async def confirm_selection(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected_dates", [])

    if not selected:
        await callback.answer("Ви не обрали жодної дати!", show_alert=True)
        return

    await callback.message.edit_text(
        f"Ви обрали {len(selected)} дат: \n" + "\n".join(selected)
    )
    await state.clear()
