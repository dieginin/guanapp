from typing import Callable, Optional

import flet as ft

import components as cp
import controllers as cl
from models import Customer


class NuevaCotizacionView(ft.View):
    def __init__(self, page: ft.Page, customer: Customer) -> None:
        super().__init__()
        page.theme = ft.Theme(color_scheme_seed="orange")
        page.title = "GuanApp • Nueva Cotización"

        self.customer = customer

        self.__init__config()
        self.__init_components__()

    def __init__config(self) -> None:
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = 0

    def __init_components__(self) -> None:
        fb = cl.Firebase()
        title = cp.Title(f"Cotización N. {fb.next_quote_index:,}")
        name = cp.Subtitle(self.customer.name)
        address = cp.RegularText(self.customer.address, 32)

        coti_btn = cp.PrimaryButton("Cotizar", on_click=self.__cotizar)
        back_btn = cp.CustomButton("orange", "Regresar", on_click=self.__back)

        btns = cp.ButtonRow([back_btn, coti_btn])
        info = ft.Column([name, address], None, ft.CrossAxisAlignment.CENTER, -15)
        columns = ["Concepto", "Talla", "Cantidad", "Precio"]
        self.datatable = ft.DataTable(
            [
                ft.DataColumn(
                    cp.RegularText(c, 30),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                )
                for c in columns
            ],
            width=float("inf"),
            expand=True,
            divider_thickness=0,
            horizontal_lines=ft.BorderSide(1, "background"),
        )
        self.__add_row()

        vigencia_txt = cp.RegularText("Vigencia =", 32)
        self.vigencia_fld = cp.RegularField(
            "60 dias", aligned=True, on_submit=self.__cotizar, width=200
        )
        self.vigencia_fld.dense = True
        iva_txt = cp.RegularText("IVA =", 32)
        self.iva_fld = cp.NumberField(
            "0", aligned=True, allow_float=True, on_submit=self.__cotizar, width=50
        )
        self.iva_fld.dense = True
        self.iva_fld.max_length = 3

        self.total = cp.RegularText("Total = $0", 32)
        last_row = ft.Row(
            [
                ft.Row([vigencia_txt, self.vigencia_fld]),
                ft.Row([iva_txt, self.iva_fld]),
                ft.Container(self.total, width=300),
            ],
            ft.MainAxisAlignment.SPACE_AROUND,
        )
        self.controls = [title, btns, info, self.datatable, last_row]

    def __back(self, e: ft.ControlEvent) -> None:
        cl.start_loading(e.page)
        e.page.go("/cotizaciones")
        cl.finish_loading(e.page)

    def __add_row(self) -> None:
        fields = [
            cp.NameField(
                aligned=True,
                autofocus=True,
                on_change=self.__modify_concepts,
                on_submit=self.__cotizar,
                width=250,
            ),
            cp.RegularField(
                aligned=True,
                on_change=self.__modify_concepts,
                on_submit=self.__cotizar,
            ),
            cp.RegularField(
                aligned=True,
                on_change=self.__modify_concepts,
                on_submit=self.__cotizar,
            ),
            cp.NumberField(
                aligned=True,
                allow_float=True,
                on_change=self.__modify_concepts,
                on_submit=self.__cotizar,
            ),
        ]
        row = ft.DataRow([ft.DataCell(f) for f in fields])
        self.datatable.rows.append(row)  # type: ignore

    def __get_field_value(self, field: ft.TextField) -> Optional[str]:
        return field.value.strip() if field.value else None

    def __modify_concepts(self, e: ft.ControlEvent) -> None:
        rows = self.datatable.rows or []
        i = rows.index(e.control.parent.parent)
        current_row = rows[i]

        concept = self.__get_field_value(current_row.cells[0].content)  # type: ignore
        size = self.__get_field_value(current_row.cells[1].content)  # type: ignore
        qty = self.__get_field_value(current_row.cells[2].content)  # type: ignore
        uprc = self.__get_field_value(current_row.cells[3].content)  # type: ignore

        if bool(concept and size and qty and uprc):
            if len(rows) == i + 1 and len(rows) <= 4:
                self.__add_row()
        else:
            if len(rows) > i + 1:
                self.datatable.rows.pop()  # type: ignore
        self.datatable.update()
        self.__sum()

    def __sum(self) -> None:
        rows = self.datatable.rows or []
        total = 0

        for row in rows:
            qty = self.__get_field_value(row.cells[2].content)  # type: ignore
            uprc = self.__get_field_value(row.cells[3].content)  # type: ignore

            if qty and uprc:
                total += int(qty) * float(uprc)

        total = int(total) if total.is_integer() else total
        self.total.value = f"Total = ${total:,}"
        self.total.update()

    def __cotizar(self, e: ft.ControlEvent) -> None:
        rows = self.datatable.rows or []
        vigency = self.__get_field_value(self.vigencia_fld) or ""
        iva = float(self.__get_field_value(self.iva_fld) or 0)
        iva = iva / 100 if iva > 1 else iva

        concepts = []
        for i, row in enumerate(rows):
            concept_fld: ft.TextField = row.cells[0].content  # type: ignore
            size_fld: ft.TextField = row.cells[1].content  # type: ignore
            qty_fld: ft.TextField = row.cells[2].content  # type: ignore
            uprc_fld: ft.TextField = row.cells[3].content  # type: ignore

            concept = self.__get_field_value(concept_fld)
            size = self.__get_field_value(size_fld)
            qty = self.__get_field_value(qty_fld)
            uprc = self.__get_field_value(uprc_fld)

            if i == 0 or (i > 0 and (concept or size or qty or uprc)):
                if not concept:
                    concept_fld.focus()
                    return
                if not size:
                    size_fld.focus()
                    return
                if not qty:
                    qty_fld.focus()
                    return
                if not uprc:
                    uprc_fld.focus()
                    return

            concepts.append(
                {"concept": concept, "size": size, "quantity": qty, "price": uprc}
            )

        if not self.vigencia_fld.value:
            self.vigencia_fld.focus()
            return

        if not self.iva_fld.value:
            self.iva_fld.focus()
            return

        cl.start_loading(e.page)
        fb = cl.Firebase()
        res = fb.create_quote(self.customer, concepts, iva, vigency)
        cl.finish_loading(e.page)

        if res.status == "Success":
            cl.success_snackbar(e.page, res.message)
            if self.customer.email:
                self.__ask_send(e)
            else:
                self.__ask_download(e)
        else:
            cl.error_snackbar(e.page, res.message)

    def __show_dialog(
        self, page: ft.Page, title: str, handle: Callable
    ) -> ft.AlertDialog:
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            actions=[
                ft.TextButton("Si", on_click=handle),
                ft.TextButton("No", on_click=handle),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        page.open(dialog)
        return dialog

    def __ask_send(self, e: ft.ControlEvent) -> None:
        def email_handle(e: ft.ControlEvent) -> None:
            e.page.close(dialog)
            if e.control.text == "Si":
                # TODO Generar PDF y mandar correo
                cl.start_loading(e.page)
                e.page.go("/cotizaciones")
                cl.finish_loading(e.page)
            else:
                self.__ask_download(e)

        dialog = self.__show_dialog(
            e.page, "¿Quieres mandarlo por email?", email_handle
        )

    def __ask_download(self, e: ft.ControlEvent) -> None:
        def download_handle(e: ft.ControlEvent) -> None:
            e.page.close(dialog)
            if e.control.text == "Si":
                # TODO Generar PDF y descargar
                ...

            cl.start_loading(e.page)
            e.page.go("/cotizaciones")
            cl.finish_loading(e.page)

        dialog = self.__show_dialog(
            e.page, "¿Quieres descargar la cotización?", download_handle
        )
