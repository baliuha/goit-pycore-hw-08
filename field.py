from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Field(ABC):
    value: any


class Name(Field):
    def __init__(self, name: str):
        if not name:
            raise ValueError("Name is required field")
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone: str):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(phone)


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value: str):
        try:
            parsed = datetime.strptime(value, self.DATE_FORMAT)
            super().__init__(parsed)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY instead")

    def __str__(self) -> str:
        return self.value.strftime(self.DATE_FORMAT)
