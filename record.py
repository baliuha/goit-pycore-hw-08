from field import Name, Phone, Birthday


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_num: str):
        if not self.find_phone(phone_num):
            self.phones.append(Phone(phone_num))

    def remove_phone(self, phone_num: str):
        phone = self.find_phone(phone_num)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_phone_num: str, new_phone_num: str):
        phone = self.find_phone(old_phone_num)
        if not phone:
            raise ValueError(f"Phone '{old_phone_num}' is not found")
        index = self.phones.index(phone)
        self.phones[index] = Phone(new_phone_num)

    def find_phone(self, phone_num: str) -> Phone | None:
        for phone in self.phones:
            if phone.value == phone_num:
                return phone
        return None

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def __str__(self) -> str:
        birthday_str = str(self.birthday) if self.birthday else "unknown"
        phones_str = "; ".join(p.value for p in self.phones) or "no phones"

        return f"Contact name: {self.name.value}, birthday: {birthday_str}, phones: {phones_str}"
