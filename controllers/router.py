import os

import flet as ft

from .firebase import Firebase


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
                    route = "/" + attr_name.lower()

                    if route.endswith("view"):
                        route = route[:-4]
                    if route == "/home":
                        route = "/"

                    routes[route] = attr

    return routes


class PageNotFoundView(ft.View):
    def __init__(self, *_) -> None:
        super().__init__()
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
        troute = ft.TemplateRoute(e.route)
        e.page.views.clear()
        routes = get_routes("views")

        if troute.route.count("/") == 1:
            self.__handle_standard_route(e, troute, routes)
        else:
            self.__handle_dynamic_route(e, troute, routes)
        e.page.update()

    def __handle_standard_route(
        self, e: ft.RouteChangeEvent, troute: ft.TemplateRoute, routes: dict
    ) -> None:
        route = troute.route
        view = routes.get(route, PageNotFoundView)
        e.page.views.append(view(e.page))

    def __handle_dynamic_route(
        self, e: ft.RouteChangeEvent, troute: ft.TemplateRoute, routes: dict
    ) -> None:
        if troute.match("/nuevacotizacion/:uid"):
            customer = Firebase().get_customer_by_uid(troute.uid)  # type: ignore
            route = troute.route.split("/")[0]
            view = routes.get(route, PageNotFoundView)
            e.page.views.append(view(e.page, customer))
