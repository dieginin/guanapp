from typing import Literal


class Response:
    def __init__(self, status: Literal["Success", "Error"], message: str) -> None:
        self.status = status
        self.message = message
