from datetime import datetime

import flet as ft

import components as cp
import controllers as cl


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
        self.padding = 0

    def __init_components__(self) -> None:
        title = cp.Title("Cotizaciones")

        home_btn = cp.CustomButton("blue", "Inicio", on_click=self.__home)
        new_btn = cp.PrimaryButton("Nuevo Cliente", on_click=self.__new)

        self.clients_lst = ft.ListView(expand=True)
        self.no_customers = ft.Container(
            cp.RegularText("Aun no hay clientes registrados"),
            alignment=ft.alignment.center,
            expand=True,
        )
        self.__get_customers()

        btns = cp.ButtonRow([home_btn, new_btn])

        self.controls = [title, btns, self.clients_lst, self.no_customers]

    def __get_customers(self) -> None:
        fb = cl.Firebase()
        customers = fb.customers_list or []
        quotes = fb.quotes_list or []

        self.clients_lst.controls.clear()

        customers_with_last_quote = []
        for customer in customers:
            customer_quotes = [q for q in quotes if q.customer.uid == customer.uid]
            last_quote = customer_quotes[-1].date if customer_quotes else None
            customers_with_last_quote.append(
                {
                    "customer": customer,
                    "last_quote": last_quote,
                    "quotes": customer_quotes,
                }
            )

        customers_with_last_quote.sort(
            key=lambda x: (
                x["last_quote"] if x["last_quote"] is not None else datetime.max
            )
        )

        for entry in customers_with_last_quote:
            customer = entry["customer"]
            last_quote = (
                entry["last_quote"].strftime("%d de %B del %Y a las %-I:%M %p")
                if entry["last_quote"]
                else "S/C"
            )
            quotes = entry["quotes"][-1] if entry["quotes"] else None

            self.clients_lst.controls.insert(
                0,
                ft.ListTile(
                    cp.RegularText(customer.name, 32),
                    cp.RegularText(f"Última cotización: {last_quote}", 16),
                    leading=ft.Icon("person_pin", size=50),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Descargar última cotización",
                                disabled=not quotes,
                                on_click=self.__save_quote,
                            )
                        ],
                    ),
                    on_click=self.__customer_click,
                    data=(customer, quotes),
                ),
            )

        self.clients_lst.visible = len(self.clients_lst.controls) > 0
        self.no_customers.visible = len(self.clients_lst.controls) <= 0

    def __home(self, e: ft.ControlEvent) -> None:
        e.page.go("/")

    def __new(self, e: ft.ControlEvent) -> None:
        def _save(_) -> None:
            name = name_fld.value.strip() if name_fld.value else None
            address = address_fld.value.strip() if address_fld.value else None
            email = email_fld.value.strip() if email_fld.value else None

            if not name:
                name_fld.error_text = "Ingresa el nombre"
                name_fld.focus()
                return
            if not address:
                address_fld.error_text = "Ingresa la dirección"
                address_fld.focus()
                return

            client_sheet.open = False
            e.page.update()

            cl.start_loading(e.page)
            fb = cl.Firebase()
            res = fb.create_customer(name, address, email)
            cl.finish_loading(e.page)

            if res.status == "Success":
                cl.start_loading(e.page)
                self.__get_customers()
                cl.finish_loading(e.page)

                self.clients_lst.scroll_to(0, duration=1000)
                self.no_customers.update()
                cl.success_snackbar(e.page, res.message)
            else:
                cl.error_snackbar(e.page, res.message)

        txt = cp.RegularText("Por favor ingresa los datos del cliente", 30)
        name_fld = cp.NameField(label="Nombre", autofocus=True, on_submit=_save)
        address_fld = cp.AddressField(label="Dirección", on_submit=_save)
        email_fld = cp.EmailField(label="Email (Opcional)", on_submit=_save)
        body = [txt, name_fld, address_fld, email_fld]
        client_sheet = cp.BottomSheet("Nuevo Cliente", body, "Guardar", _save)

        e.page.open(client_sheet)

    def __customer_click(self, e: ft.ControlEvent) -> None:
        cl.start_loading(e.page)
        e.page.go(f"/nuevacotizacion/{e.control.data[0]}")
        cl.finish_loading(e.page)

    def __save_quote(self, e: ft.ControlEvent) -> None:
        quote = e.control.parent.parent.data[1]
        path = cl.Pdf().generate_quote(quote)
        cl.success_snackbar(e.page, f"Cotización descargada en {path}")
