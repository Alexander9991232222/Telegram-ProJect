import calendar

import pytest

from src.enums import CalendarActions, CalendarIcons
from src.models import CalendarButtonModel
from src.services.calendar_generator import (
    _check_all_days_selected_in_month,
    _generate_confirmation_button,
    _generate_days_buttons,
    _generate_navigation_buttons,
    _generate_weeks_month_buttons,
    _get_days_in_week,
    _get_name_month_by_index,
    _get_weeks_in_year,
    generate_calendar,
)


@pytest.fixture
def year_and_month() -> tuple[int, int]:
    return (2023, 1)


def test_generate_navigation_buttons(year_and_month: tuple[int, int]) -> None:
    year, month = year_and_month
    prev_button, month_button, next_button = _generate_navigation_buttons(year, month)

    assert len(_generate_navigation_buttons(year, month)) == 3
    assert isinstance(prev_button, CalendarButtonModel)
    assert isinstance(month_button, CalendarButtonModel)
    assert isinstance(next_button, CalendarButtonModel)
    assert prev_button == _prev_button_config()
    assert month_button == _month_button_config(year, month)
    assert next_button == _next_button_config()


def _prev_button_config() -> CalendarButtonModel:
    return CalendarButtonModel(
        id="cal_nab_back_month_button",
        row=0,
        col=0,
        text=CalendarIcons.NAV_BACK,
        action=CalendarActions.PREV,
        callback_data="callendar_prev_month_callback",
    )


def _month_button_config(year: int, month: int) -> CalendarButtonModel:
    return CalendarButtonModel(
        id="cal_month_button",
        row=0,
        col=1,
        text=f"{_get_name_month_by_index(month)} {year}",
        action=CalendarActions.MONTH,
        callback_data=f"month:{month:02d}-{year}",
    )


def _next_button_config() -> CalendarButtonModel:
    return CalendarButtonModel(
        id="cal_nav_next_month_button",
        row=0,
        col=1,
        text=CalendarIcons.NAV_NEXT,
        action=CalendarActions.NEXT,
        callback_data="callendar_next_month_callback",
    )


def test_check_all_days_selected_in_month(year_and_month: tuple[int, int]) -> None:
    col = 1
    year, month = year_and_month
    selected_days = _selected_all_days_by_col(year, month, col)

    assert _check_all_days_selected_in_month(year, month, selected_days, col)


def test_check_is_not_all_days_selecte_in_month(
    year_and_month: tuple[int, int],
) -> None:
    col = 1
    year, month = year_and_month
    selected_days = _selected_all_days_by_col(year, month, col)

    selected_days.pop(1)

    assert not _check_all_days_selected_in_month(year, month, selected_days, col)


def _selected_all_days_by_col(year: int, month: int, col: int) -> list[str]:
    weeks = calendar.monthcalendar(year, month)

    return [f"{day:02d}-{month:02d}-{year}" for week in weeks if (day := week[col]) > 0]


def test_confirmation_button() -> None:
    conf_button = _generate_confirmation_button()

    assert isinstance(conf_button, CalendarButtonModel)
    assert conf_button == _get_confirmatio_button_config()


def _get_confirmatio_button_config() -> CalendarButtonModel:
    return CalendarButtonModel(
        id="confirmation_button",
        text="Підтвердити",
        action=CalendarActions.IGNORE,
        callback_data="cal_confirm_callback",
        col=0,
        row=8,
    )


@pytest.mark.parametrize(
    "index, month_name",
    [
        (-1, ""),
        (0, ""),
        (1, "Січень"),
        (2, "Лютий"),
        (3, "Березень"),
        (4, "Квітень"),
        (5, "Травень"),
        (6, "Червень"),
        (7, "Липень"),
        (8, "Серпень"),
        (9, "Вересень"),
        (10, "Жовтень"),
        (11, "Листопад"),
        (12, "Грудень"),
        (13, ""),
    ],
)
def test_get_name_month_by_index(index: int, month_name: str) -> None:
    assert _get_name_month_by_index(index) == month_name


def test_get_weeks_in_year(year_and_month: tuple[int, int]) -> None:
    year, month = year_and_month

    expected_weeks = calendar.monthcalendar(year, month)
    actual_weeks = _get_weeks_in_year(year, month)

    assert expected_weeks == actual_weeks


@pytest.mark.parametrize(
    "index, expected_name",
    [
        (0, "Пн"),
        (1, "Вт"),
        (2, "Ср"),
        (3, "Чт"),
        (4, "Пт"),
        (5, "Сб"),
        (6, "Нд"),
        (7, " "),
    ],
)
def test_check_days_in_week(index: int, expected_name: str) -> None:
    actual_name_days = _get_days_in_week()

    assert len(actual_name_days) == 8
    assert actual_name_days[index] == expected_name


@pytest.mark.parametrize("index, exp_day_name", [(0, "Пн")])
def test_generate_days_buttons_is_not_selected(
    year_and_month: tuple[int, int], index: int, exp_day_name: str
) -> None:
    year, month = year_and_month
    actual_days = _generate_days_buttons(year, month, [])

    day_conf = actual_days[index]

    assert len(actual_days) == 8
    assert isinstance(day_conf, CalendarButtonModel)
    assert day_conf.text == exp_day_name
    assert day_conf.id == f"weekday_header_{index}-{month:02d}-{year}"
    assert day_conf.action == CalendarActions.COL
    assert not day_conf.is_selected
    assert day_conf.row == 1
    assert day_conf.col == index
    assert day_conf.callback_data == f"cal_days_in_month:{index}-{month:02d}-{year}"


@pytest.mark.parametrize("index", [(3)])
def test_generate_days_button_is_selected(
    year_and_month: tuple[int, int], index: int
) -> None:
    year, month = year_and_month
    selected_days = _selected_all_days_by_col(year, month, index)
    actual_days = _generate_days_buttons(year, month, selected_days)

    selected_day = actual_days[index]

    assert selected_day.is_selected


@pytest.mark.parametrize("index, exp_day_name", [(7, " ")])
def test_generate_days_button_empty(
    year_and_month: tuple[int, int], index: int, exp_day_name: str
) -> None:
    year, month = year_and_month

    actual_days = _generate_days_buttons(year, month, [])
    actual_day = actual_days[index]

    assert actual_day.text == exp_day_name
    assert actual_day.id == f"empty_header_{index}-{month:02d}-{year}"
    assert actual_day.callback_data == "ignore"
    assert actual_day.action == CalendarActions.IGNORE
    assert not actual_day.is_selected
    assert actual_day.row == 1
    assert actual_day.col == index


def test_generate_weeks_in_month_buttons_length(
    year_and_month: tuple[int, int],
) -> None:
    year, month = year_and_month

    weeks = _generate_weeks_month_buttons(year, month, [])

    assert len(weeks) == 6


def test_generate_weeks_in_month_buttons_is_not_selected(
    year_and_month: tuple[int, int],
) -> None:
    year, month = year_and_month

    weeks = _generate_weeks_month_buttons(year, month, [])

    for week in weeks:
        for day in week:
            assert not day.is_selected


def test_generate_weeks_in_month_buttons_is_selected(
    year_and_month: tuple[int, int],
) -> None:
    year, month = year_and_month

    selected_all_day = _selected_all_days(year, month)
    weeks = _generate_weeks_month_buttons(year, month, selected_all_day)

    for week in weeks:
        for day in week:
            if day.text == " " or day.text.__contains__("н"):
                continue
            assert day.is_selected


def _selected_all_days(year: int, month: int) -> list[str]:
    return [f"{day:02d}-{month:02d}-{year}" for day in range(1, 32)]


def test_generate_weeks_month_buttons_with_padding(
    year_and_month: tuple[int, int],
) -> None:
    year, month = year_and_month
    selected = ["01-01-2023"]

    weeks = _generate_weeks_month_buttons(year, month, selected)

    first_week = weeks[0]

    assert first_week[0].text == " "
    assert first_week[0].action == CalendarActions.IGNORE

    assert first_week[6].text == CalendarIcons.SELECTED
    assert first_week[6].is_selected is True

    assert first_week[7].text == "1н"


def test_generate_calendar_minimal_params(year_and_month: tuple[int, int]) -> None:
    year, month = year_and_month
    result = generate_calendar(year, month)

    assert len(result) > 0
    for row in result:
        for btn in row:
            assert isinstance(btn, CalendarButtonModel)
