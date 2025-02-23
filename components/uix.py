from typing import Callable

import flet as ft

from .buttons import CancelButton, PrimaryButton
from .text import Title


class ButtonRow(ft.Row):
    def __init__(self, buttons: list[ft.ElevatedButton]) -> None:
        super().__init__()
        self.controls = buttons
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 75


class BottomSheet(ft.BottomSheet):
    def __init__(
        self,
        title: str,
        controls: list[ft.Control],
        btn_label: str,
        btn_function: Callable,
    ) -> None:
        sav_btn = PrimaryButton(btn_label, on_click=btn_function)
        can_btn = CancelButton("Cancelar", on_click=lambda e: e.page.close(self))

        body = ft.Column(
            controls, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=25
        )
        btns = ButtonRow([sav_btn, can_btn])

        super().__init__(
            ft.Container(
                padding=50,
                content=ft.Column(
                    [Title(title), body, btns],
                    ft.MainAxisAlignment.SPACE_BETWEEN,
                    ft.CrossAxisAlignment.CENTER,
                    spacing=25,
                ),
            )
        )
        self.is_scroll_controlled = True
