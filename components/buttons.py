from typing import Callable, Literal, Optional

from flet import ButtonStyle, ElevatedButton


class __Button(ElevatedButton):
    def __init__(
        self,
        text: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_click: Optional[Callable] = None,
    ) -> None:
        super().__init__()
        self.text = text
        self.autofocus = autofocus
        self.on_click = on_click
        self.height = 45
        self.width = 185

    def _set_style(self, color: str, light: bool) -> None:
        self.style = (
            ButtonStyle(
                color=f"on{color}container",
                bgcolor=f"{color}container",
                overlay_color=f"{color},.1",
            )
            if light
            else ButtonStyle(
                color=f"on{color}", bgcolor=color, overlay_color=f"{color}container,.1"
            )
        )


class PrimaryButton(__Button):
    def __init__(
        self,
        text: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_click: Optional[Callable] = None,
        light: bool = False,
    ) -> None:
        super().__init__(text, autofocus, on_click)
        self._set_style("primary", light)


class SecondaryButton(__Button):
    def __init__(
        self,
        text: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_click: Optional[Callable] = None,
        light: bool = False,
    ) -> None:
        super().__init__(text, autofocus, on_click)
        self._set_style("secondary", light)


class TertiaryButton(__Button):
    def __init__(
        self,
        text: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_click: Optional[Callable] = None,
        light: bool = False,
    ) -> None:
        super().__init__(text, autofocus, on_click)
        self._set_style("tertiary", light)


class CancelButton(__Button):
    def __init__(
        self,
        text: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_click: Optional[Callable] = None,
        light: bool = False,
    ) -> None:
        super().__init__(text, autofocus, on_click)
        self._set_style("error", light)


ColorType = Literal[
    "red",
    "pink",
    "purple",
    "deeppurple",
    "indigo",
    "blue",
    "lightblue",
    "cyan",
    "teal",
    "green",
    "lightgreen",
    "lime",
    "yellow",
    "amber",
    "orange",
    "deeporange",
    "brown",
    "bluegrey",
    "grey",
]


class CustomButton(__Button):
    def __init__(
        self,
        color: ColorType,
        text: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_click: Optional[Callable] = None,
    ) -> None:
        super().__init__(text, autofocus, on_click)
        self.style = ButtonStyle(
            color=f"{color}50", bgcolor=color, overlay_color=f"{color}100,.15"
        )
