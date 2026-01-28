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
        self.col = col
        self.is_selected = is_selected
        self.row = row
        self.callback_data = callback_data
        self.action = action

        self.text = f"{CalendarIcons.SELECTED}" if is_selected else text
