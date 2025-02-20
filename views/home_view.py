import flet as ft

from components import CustomButton, PrimaryButton, Subtitle, Title
from controllers import error_snackbar


class _ButtonRow(ft.Row):
    def __init__(self, buttons: list[ft.ElevatedButton]) -> None:
        super().__init__()
        self.controls = buttons
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 75


class HomeView(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        page.theme = ft.Theme(color_scheme_seed="blue")
        page.title = "GuanApp"

        self.__init__config()
        self.__init_components__()

    def __init__config(self) -> None:
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def __init_components__(self) -> None:
        title = Title("GuanApp")
        subtitle = Subtitle("¿Qué quieres hacer hoy?")

        cli_btn = PrimaryButton("Clientes", on_click=self.__clientes)
        cons_btn = CustomButton("green", "Constancias", on_click=self.__constancias)
        coti_btn = CustomButton("orange", "Cotizaciones", on_click=self.__cotizaciones)

        btns_one = _ButtonRow([cons_btn, coti_btn])
        btns_two = _ButtonRow([cli_btn])

        self.controls = [title, subtitle, ft.Container(height=35), btns_one, btns_two]

    def __clientes(self, e: ft.ControlEvent) -> None:
        # TODO Agregar sección clientes
        error_snackbar(
            e.page, "Esta sección aún no está lista, contacta al programador"
        )

    def __constancias(self, e: ft.ControlEvent) -> None:
        # TODO Agregar sección constancias
        error_snackbar(
            e.page, "Esta sección aún no está lista, contacta al programador"
        )

    def __cotizaciones(self, e: ft.ControlEvent) -> None:
        e.page.go("/cotizaciones")
