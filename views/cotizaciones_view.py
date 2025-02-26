import flet as ft

import components as cp
from controllers import Firebase, error_snackbar, success_snackbar


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
        self.__get_customers()

        btns = cp.ButtonRow([home_btn, new_btn])

        self.controls = [title, btns, self.clients_lst]

    def __get_customers(self) -> None:
        fb = Firebase()
        customers = fb.customers_list
        self.clients_lst.controls.clear()

        if customers:
            for customer in customers:
                self.clients_lst.controls.insert(
                    0,
                    ft.ListTile(
                        cp.RegularText(customer.name, 32),
                        cp.RegularText(
                            "Última cotización: S/D", 16
                        ),  # TODO Obtener ultima cotizacion
                        leading=ft.Icon("person_pin", size=50),
                        on_click=self.__customer_click,
                        data=customer,
                    ),
                )

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
            e.page.overlay.append(ft.ProgressBar())
            e.page.update()

            fb = Firebase()
            res = fb.create_customer(name, address, email)

            e.page.overlay.pop()
            if res.status == "Success":
                self.__get_customers()
                self.clients_lst.update()
                success_snackbar(e.page, res.message)
            else:
                error_snackbar(e.page, res.message)

        txt = cp.RegularText("Por favor ingresa los datos del cliente", 30)
        name_fld = cp.NameField(label="Nombre", autofocus=True, on_submit=_save)
        address_fld = cp.AddressField(label="Dirección", on_submit=_save)
        email_fld = cp.EmailField(label="Email (Opcional)", on_submit=_save)
        body = [txt, name_fld, address_fld, email_fld]
        client_sheet = cp.BottomSheet("Nuevo Cliente", body, "Guardar", _save)

        e.page.open(client_sheet)

    def __customer_click(self, e: ft.ControlEvent) -> None:
        e.page.go(f"/nuevacotizacion/{e.control.data}")
