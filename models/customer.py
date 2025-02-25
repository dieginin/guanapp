from typing import Optional


class Customer:
    def __init__(
        self, uid: str, name: str, address: str, email: Optional[str] = None
    ) -> None:
        self.uid = uid
        self.name = name
        self.address = address
        self.email = email

    def to_dict(self) -> dict:
        return {"name": self.name, "address": self.address, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        return cls(data["uid"], data["name"], data["address"], data.get("email"))
