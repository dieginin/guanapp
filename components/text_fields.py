from typing import Any, Callable, Optional

import flet as ft


class __TextField(ft.TextField):
    def __init__(
        self,
        value: Optional[Any] = None,
        label: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_change: Optional[Callable] = None,
        on_click: Optional[Callable] = None,
        on_submit: Optional[Callable] = None,
        on_focus: Optional[Callable] = None,
        on_blur: Optional[Callable] = None,
        width: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.value = value
        self.label = label
        self.autofocus = autofocus
        self._pre_on_change = on_change
        self.on_change = self._on_change
        self.on_click = on_click
        self.on_submit = on_submit
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.width = width
        self.border = ft.InputBorder.UNDERLINE
        self.focused_border_width = 3

    def _on_change(self, e: ft.ControlEvent) -> None:
        self.error_text = None
        self.update()

        if self._pre_on_change:
            self._pre_on_change(e)


class RegularField(__TextField):
    def __init__(
        self,
        value: Optional[str] = None,
        label: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_change: Optional[Callable] = None,
        on_click: Optional[Callable] = None,
        on_submit: Optional[Callable] = None,
        on_focus: Optional[Callable] = None,
        on_blur: Optional[Callable] = None,
        width: Optional[int] = None,
    ) -> None:
        super().__init__(
            value,
            label,
            autofocus,
            on_change,
            on_click,
            on_submit,
            on_focus,
            on_blur,
            width,
        )
        self.keyboard_type = ft.KeyboardType.TEXT


class NameField(__TextField):
    def __init__(
        self,
        value: Optional[str] = None,
        label: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_change: Optional[Callable] = None,
        on_click: Optional[Callable] = None,
        on_submit: Optional[Callable] = None,
        on_focus: Optional[Callable] = None,
        on_blur: Optional[Callable] = None,
        width: Optional[int] = None,
    ) -> None:
        super().__init__(
            value,
            label,
            autofocus,
            on_change,
            on_click,
            on_submit,
            on_focus,
            on_blur,
            width,
        )
        self.autofill_hints = ft.AutofillHint.NAME
        self.capitalization = ft.TextCapitalization.WORDS
        self.input_filter = ft.InputFilter(
            r"^[A-Za-z'\.\-\s]+|$"
        )  # BUG Filter not working
        self.keyboard_type = ft.KeyboardType.NAME


class AddressField(__TextField):
    def __init__(
        self,
        value: Optional[str] = None,
        label: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_change: Optional[Callable] = None,
        on_click: Optional[Callable] = None,
        on_submit: Optional[Callable] = None,
        on_focus: Optional[Callable] = None,
        on_blur: Optional[Callable] = None,
        width: Optional[int] = None,
    ) -> None:
        super().__init__(
            value,
            label,
            autofocus,
            on_change,
            on_click,
            on_submit,
            on_focus,
            on_blur,
            width,
        )
        self.autofill_hints = ft.AutofillHint.ADDRESS_CITY_AND_STATE
        self.capitalization = ft.TextCapitalization.SENTENCES
        self.input_filter = ft.InputFilter(
            r"^[A-Za-z0-9'\.\-\s\,]+|$"
        )  # BUG Filter not working
        self.keyboard_type = ft.KeyboardType.STREET_ADDRESS


class NumberField(__TextField):
    def __init__(
        self,
        value: Optional[str] = None,
        label: Optional[str] = None,
        autofocus: Optional[bool] = None,
        allow_float: Optional[bool] = False,
        on_change: Optional[Callable] = None,
        on_click: Optional[Callable] = None,
        on_submit: Optional[Callable] = None,
        on_focus: Optional[Callable] = None,
        on_blur: Optional[Callable] = None,
        width: Optional[int] = None,
    ) -> None:
        super().__init__(
            value,
            label,
            autofocus,
            on_change,
            on_click,
            on_submit,
            on_focus,
            on_blur,
            width,
        )
        self.input_filter = ft.InputFilter(
            r"^([0-9]*[.])?[0-9]+|$" if allow_float else r"^[0-9]+|$"
        )  # BUG Filter not working
        self.keyboard_type = ft.KeyboardType.NUMBER


class EmailField(__TextField):
    def __init__(
        self,
        value: Optional[str] = None,
        label: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_change: Optional[Callable] = None,
        on_click: Optional[Callable] = None,
        on_submit: Optional[Callable] = None,
        on_focus: Optional[Callable] = None,
        on_blur: Optional[Callable] = None,
        width: Optional[int] = None,
    ) -> None:
        super().__init__(
            value,
            label,
            autofocus,
            on_change,
            on_click,
            on_submit,
            on_focus,
            on_blur,
            width,
        )
        self.autofill_hints = ft.AutofillHint.EMAIL
        self.input_filter = ft.InputFilter(
            r"^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}|$"
        )  # BUG Filter not working
        self.keyboard_type = ft.KeyboardType.EMAIL
