import os

import flet as ft


def get_routes(directory: str) -> dict:
    routes = {}

    for file in os.listdir(directory):
        if file.endswith(".py"):
            module_name = file[:-3]
            module = __import__(f"{directory}.{module_name}", fromlist=[module_name])

            for attr_name in dir(module):
                attr = getattr(module, attr_name)

                if (
                    isinstance(attr, type)
                    and issubclass(attr, ft.View)
                    and attr != ft.View
                ):
                    route = "/" + attr_name[0].lower() + attr_name[1:]

                    if route.endswith("View"):
                        route = route[:-4]
                    if route == "/home":
                        route = "/"

                    routes[route] = attr

    return routes


class PageNotFoundView(ft.View):
    def __init__(self) -> None:
        super().__init__()
        self.route = "/pageNotFound"

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

        self.controls = [ft.Text("Page Not Found", size=32, weight=ft.FontWeight.BOLD)]
        self.floating_action_button = ft.FloatingActionButton(
            icon="home", on_click=lambda e: e.page.go("/")
        )


class Router:
    def __init__(self, page: ft.Page) -> None:
        page.on_route_change = self.on_route_change
        page.go("/")

    def on_route_change(self, e: ft.RouteChangeEvent) -> None:
        e.page.views.clear()
        routes = get_routes("views")

        if e.route in routes:
            e.page.views.append(routes[e.route]())
        else:
            e.page.views.append(PageNotFoundView())

        e.page.update()
