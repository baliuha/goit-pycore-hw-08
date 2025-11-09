import calendar
from collections import UserDict
from datetime import datetime, date, timedelta
from record import Record


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    @staticmethod
    def __is_leap_birthday(birthday: datetime.date, current_year: int) -> bool:
        return (birthday.month == 2
                and birthday.day == 29
                and not calendar.isleap(current_year))

    @staticmethod
    def __move_date_to_monday(congrats_date: datetime.date) -> datetime.date:
        if congrats_date.weekday() == 5:
            congrats_date += timedelta(days=2)
        elif congrats_date.weekday() == 6:
            congrats_date += timedelta(days=1)

        return congrats_date

    def get_upcoming_birthdays(self) -> list[dict]:
        today = datetime.today()
        one_week_later = today + timedelta(days=7)
        congrats_list = []

        for user in self.data.values():
            if not user.birthday:
                continue

            birthday = user.birthday.value
            if self.__is_leap_birthday(birthday, today.year):
                birthday_this_year = date(today.year, 2, 28)
            else:
                birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if today <= birthday_this_year <= one_week_later:
                congrats_date = self.__move_date_to_monday(birthday_this_year)
                congrats_list.append({
                    "name": user.name.value,
                    "congratulation_date": congrats_date.strftime(user.birthday.DATE_FORMAT)
                })

        return congrats_list
