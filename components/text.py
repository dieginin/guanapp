from typing import Optional

from flet import FontWeight, Text


class __Text(Text):
    def __init__(self, value: Optional[str] = None) -> None:
        super().__init__()
        self.value = value
        self.weight = FontWeight.W_100


class Title(__Text):
    def __init__(self, value: Optional[str] = None) -> None:
        super().__init__(value)
        self.color = "primary"
        self.size = 76


class Subtitle(__Text):
    def __init__(self, value: Optional[str] = None) -> None:
        super().__init__(value)
        self.color = "outline"
        self.size = 60


class RegularText(__Text):
    def __init__(self, value: Optional[str] = None, size: int = 48) -> None:
        super().__init__(value)
        self.color = "outline"
        self.size = size
