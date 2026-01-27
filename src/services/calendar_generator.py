import calendar

from src.enums import CalendarActions, CalendarIcons
from src.models.calendar_button_model import CalendarButtonModel


def generate_calendar(year: int, month: int) -> list[list[CalendarButtonModel]]:
    result: list[list[CalendarButtonModel]] = []

    result.append(_generate_navigation_buttons(year, month))
    result.append(_generate_days_buttons(year, month))
    result = result + _generate_days_in_month_buttons(year, month)

    return result


def _generate_navigation_buttons(year: int, month: int) -> list[CalendarButtonModel]:
    previos_month_button = CalendarButtonModel(
        id="cal_nab_back_month_button",
        row=0,
        col=0,
        text=CalendarIcons.NAV_BACK,
        action=CalendarActions.PREV,
        callback_data="callendar_prev_month_callback",
    )

    month_button = CalendarButtonModel(
        id="cal_month_button",
        row=0,
        col=1,
        text=_get_name_month_by_index(month),
        action=CalendarActions.MONTH,
        callback_data=f"month:{month:02d}-{year}",
    )

    next_month_button = CalendarButtonModel(
        id="cal_nav_next_month_button",
        row=0,
        col=1,
        text=CalendarIcons.NAV_NEXT,
        action=CalendarActions.NEXT,
        callback_data="callendar_next_month_callback",
    )

    return [previos_month_button, month_button, next_month_button]


def _generate_days_buttons(year: int, month: int) -> list[CalendarButtonModel]:
    return [
        CalendarButtonModel(
            id=f"{i}-{month:02d}-{year}",
            text=day,
            row=1,
            col=i,
            action=CalendarActions.COL,
            callback_data=f"cal_days_in_month:{i}-{month:02d}-{year}",
        )
        if day != " "
        else CalendarButtonModel(
            id="ignore_button",
            row=1,
            col=i,
            text=day,
            callback_data="ignore",
            action=CalendarActions.IGNORE,
        )
        for i, day in enumerate(_get_days_in_week())
    ]


def _generate_days_in_month_buttons(
    year: int, month: int
) -> list[list[CalendarButtonModel]]:
    result: list[list[CalendarButtonModel]] = []

    for row, week in enumerate(_get_weeks_in_year(year, month)):
        days_buttons: list[CalendarButtonModel] = []

        for col, day in enumerate(week):
            if day == 0:
                days_buttons.append(
                    CalendarButtonModel(
                        id="ignore_button_{row}_{col}",
                        col=col,
                        row=row + 2,
                        text=" ",
                        action=CalendarActions.IGNORE,
                        callback_data="ignore",
                    )
                )
            else:
                days_buttons.append(
                    CalendarButtonModel(
                        id=f"{day:02d}-{month:02d}-{year}",
                        text=str(day),
                        action=CalendarActions.DAY,
                        col=col,
                        row=row + 2,
                        callback_data=f"cal_day:{day:02d}-{month:02d}-{year}",
                    )
                )
        days_buttons.append(
            CalendarButtonModel(
                id=f"{row}-{month:02d}-{year}",
                text=f"{row + 1}н",
                action=CalendarActions.ROW,
                row=row + 1,
                col=7,
                callback_data=f"cal_week_days:{row}-{month:02d}-{year}",
            )
        )

        result.append(days_buttons)

    return result


def _get_days_in_week() -> list[str]:
    return ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд", " "]


def _get_weeks_in_year(year: int, month: int) -> list[list[int]]:
    return calendar.monthcalendar(year, month)


def _get_name_month_by_index(month_index: int) -> str:
    return [
        "",
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
    ][month_index]
