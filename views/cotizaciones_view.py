import flet as ft

from components import PrimaryButton, Title
from components.buttons import CustomButton


class _ButtonRow(ft.Row):
    def __init__(self, buttons: list[ft.ElevatedButton]) -> None:
        super().__init__()
        self.controls = buttons
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 75


class CotizacionesView(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        page.theme = ft.Theme(color_scheme_seed="orange")
        page.title = "GuanApp • Cotizaciones"

        self.__init__config()
        self.__init_components__()

    def __init__config(self) -> None:
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def __init_components__(self) -> None:
        title = Title("Cotizaciones")

        hom_btn = CustomButton("blue", "Inicio", on_click=self.__home)
        nue_btn = PrimaryButton("Nuevo Cliente", on_click=self.__nueva)

        btns = _ButtonRow([hom_btn, nue_btn])

        self.controls = [title, ft.Container(height=35), btns]

    def __home(self, e: ft.ControlEvent) -> None:
        e.page.go("/")

    def __nueva(self, e: ft.ControlEvent) -> None:
        e.page.go("/nuevacotizacion")
