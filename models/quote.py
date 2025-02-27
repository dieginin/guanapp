from dataclasses import dataclass
from datetime import datetime

from .customer import Customer


@dataclass
class Concept:
    concept: str
    quantity: int
    size: str
    price: str

    def to_dict(self) -> dict:
        return {
            "concept": self.concept,
            "quantity": self.quantity,
            "size": self.size,
            "price": self.price,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Concept":
        return cls(data["concept"], data["quantity"], data["size"], data["price"])


@dataclass
class Quote:
    folio: str
    concepts: list[Concept]
    customer: Customer
    date: datetime

    def to_dict(self) -> dict:
        return {
            "concepts": [c.to_dict() for c in self.concepts],
            "customer": self.customer.uid,
            "date": self.date.strftime("%d/%m/%Y %H:%M:%S"),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quote":
        from controllers import Firebase

        return cls(
            data["folio"],
            [Concept.from_dict(c) for c in data["concepts"]],
            Firebase().get_customer_by_uid(data["customer"]),
            datetime.strptime(data["date"], "%d/%m/%Y %H:%M:%S"),
        )
