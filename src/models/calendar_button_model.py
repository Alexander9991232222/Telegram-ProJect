from src.enums import CalendarActions, CalendarIcons


class CalendarButtonModel:
    text: str
    col: int
    row: int
    is_selected: bool
    callback_data: str
    action: CalendarActions
    id: str

    def __init__(
        self,
        id: str,
        text: str,
        callback_data: str,
        col: int,
        row: int,
        action: CalendarActions,
        is_selected: bool = False,
    ) -> None:
        self.id = id
        self.text = text
        self.col = col
        self.row = row
        self.is_selected = is_selected
        self.callback_data = callback_data
        self.action = action

    def set_selected(self, is_selected: bool) -> None:
        noChangeAction: list[CalendarActions] = [
            CalendarActions.IGNORE,
            CalendarActions.MONTH,
            CalendarActions.CONFIRM,
            CalendarActions.PREV,
            CalendarActions.NEXT,
        ]

        if self.action in noChangeAction:
            return

        self.is_selected = is_selected
        self.text = (
            f"{CalendarIcons.SELECTED} {self.text}"
            if is_selected
            else self.text.replace(CalendarIcons.SELECTED, CalendarIcons.EMPTY)
        )
