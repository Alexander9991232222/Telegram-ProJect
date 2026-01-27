from enum import Enum


class CalendarActions(str, Enum):
    DAY = "day"
    COL = "col"
    ROW = "row"
    MONTH = "month"
    YEAR = "year"
    PREV = "prev"
    NEXT = "next"
    CONFIRM = "confirm"
    IGNORE = "ignore"
