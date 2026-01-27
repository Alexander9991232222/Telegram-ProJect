from src.enums import BaseStrEnum


class CalendarActions(BaseStrEnum):
    DAY = "day"
    COL = "col"
    ROW = "row"
    MONTH = "month"
    YEAR = "year"
    PREV = "prev"
    NEXT = "next"
    CONFIRM = "confirm"
    IGNORE = "ignore"
