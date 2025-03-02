import locale

import flet as ft

from controllers import Router, check_for_updates

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


class Main:
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page: ft.Page = page
        Router(self.page)
        check_for_updates(self.page)

        self.__init_window__()

    def __init_window__(self) -> None:
        self.page.window.height = 700
        self.page.window.width = 900
        self.page.window.resizable = False
        self.page.window.center()


ft.app(Main, assets_dir="assets")
