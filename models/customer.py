from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    uid: str
    name: str
    address: str
    email: Optional[str] = None

    def __str__(self) -> str:
        return self.uid

    def to_dict(self) -> dict:
        return {"name": self.name, "address": self.address, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        return cls(data["uid"], data["name"], data["address"], data.get("email"))
