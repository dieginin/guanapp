import flet as ft
from flet.core.types import ColorValue


def __show_snackbar(
    page: ft.Page, text: str, txtcolor: ColorValue, bgcolor: ColorValue
) -> None:
    txt = ft.Text(text, text_align=ft.TextAlign.CENTER, color=txtcolor)
    page.open(ft.SnackBar(txt, show_close_icon=True, bgcolor=bgcolor))


def custom_snackbar(
    page: ft.Page, text: str, txtcolor: ColorValue, bgcolor: ColorValue
) -> None:
    __show_snackbar(page, text, txtcolor, bgcolor)


def success_snackbar(page: ft.Page, message: str) -> None:
    color = "tertiary"
    __show_snackbar(page, message, f"on{color}", color)


def error_snackbar(page: ft.Page, message: str) -> None:
    color = "error"
    __show_snackbar(page, message, f"on{color}", color)


def start_loading(page: ft.Page) -> None:
    page.overlay.append(ft.ProgressBar())
    page.update()


def finish_loading(page: ft.Page) -> None:
    page.overlay.pop()
    page.update()
