import flet as ft


class ButtonRow(ft.Row):
    def __init__(self, buttons: list[ft.ElevatedButton]) -> None:
        super().__init__()
        self.controls = buttons
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 75
