from datetime import datetime
from typing import Literal, Optional

from pyrebase import pyrebase

from config import FB_CONFIG
from models import Customer, Quote


class Response:
    def __init__(self, status: Literal["Success", "Error"], message: str) -> None:
        self.status = status
        self.message = message


class Firebase:
    __fb = pyrebase.initialize_app(FB_CONFIG)
    __db = __fb.database()

    def __init__(self) -> None:
        self._cached_customers = None
        self._cached_quotes = None

    def __check_customer_existence(self, name: str) -> bool:
        if not self.customers_list:
            return False
        return any(c.name.lower() == name.lower() for c in self.customers_list)

    def __clear_customers_cache(self) -> None:
        self._cached_customers = None

    @property
    def __customers_tb(self) -> pyrebase.Database:
        return self.__db.child("customers")

    @property
    def __quotes_tb(self) -> pyrebase.Database:
        return self.__db.child("quotes")

    @property
    def customers_list(self) -> Optional[list[Customer]]:
        if self._cached_customers is None:
            try:
                self._cached_customers = [
                    Customer.from_dict({"uid": c.key()} | c.val())
                    for c in self.__customers_tb.get()
                ]
            except:
                pass
        return self._cached_customers

    @property
    def quotes_list(self) -> Optional[list[Quote]]:
        if self._cached_quotes is None:
            try:
                self._cached_quotes = [
                    Quote.from_dict({"folio": q.key()} | q.val())
                    for q in self.__quotes_tb.get()
                    if q.val() != None
                ]
            except:
                pass
        return self._cached_quotes

    @property
    def next_quote_index(self) -> int:
        return len(self.quotes_list or []) + 1

    def get_customer_by_uid(self, uid: str) -> Customer:
        customer = self.__customers_tb.child(uid).get().val()
        if type(customer) == pyrebase.OrderedDict:
            return Customer.from_dict({"uid": uid} | customer)
        return Customer(uid, "", "")

    def create_customer(
        self, name: str, address: str, email: Optional[str] = None
    ) -> Response:
        if self.__check_customer_existence(name):
            return Response("Error", f"{name} ya existe")

        self.__customers_tb.push({"name": name, "address": address, "email": email})
        self.__clear_customers_cache()
        return Response("Success", f"{name} fue añadido")

    def edit_customer(self, customer: Customer) -> Response:
        self.__customers_tb.child(customer.uid).update(customer.to_dict())
        self.__clear_customers_cache()
        return Response("Success", f"{customer.name} fue modificado")

    def delete_customer(self, customer: Customer) -> Response:
        self.__customers_tb.child(customer.uid).remove()
        self.__clear_customers_cache()
        return Response("Success", f"{customer.name} fue eliminado")

    def delete_all_customers(self) -> Response:
        deleted_amnt = len(self.__customers_tb.get().val())
        self.__customers_tb.remove()
        self.__clear_customers_cache()
        return Response("Success", f"{deleted_amnt} clientes eliminados")

    def create_quote(self, customer: Customer, concepts: list[dict]) -> Response:
        next_quote = str(self.next_quote_index)
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.__quotes_tb.child(next_quote).set(
            {"customer": customer.uid, "date": date, "concepts": concepts}
        )
        return Response("Success", f"Cotización {next_quote} fue creada")
