import pickle
from address_book import AddressBook
from record import Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ex:
            return f"Please enter valid arguments: {ex}"
        except AttributeError:
            return "Contact is not found"
        except Exception as ex:
            return f"An unexpected error occurred: {str(ex)}"
    return inner


def parse_input(user_input: str) -> tuple:
    if not user_input:
        return "", []
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


@input_error
def add_contact(args, book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("The command is - add <name> <phone>")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact is updated"
    if record is None:
        # adds contact even if phone is invalid - not a bug but feature
        record = Record(name)
        book.add_record(record)
        message = "Contact is added"
    record.add_phone(phone)

    return message


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    if len(args) < 3:
        raise ValueError("The command is - change <name> <old_phone> <new_phone>")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)

    return "Contact is updated"


@input_error
def show_phone(args: list, book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("The command is - phone <name>")
    name, *_ = args
    record = book.find(name)

    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(book: AddressBook) -> str:
    if not book:
        return "No contacts saved"
    return "\n".join(str(record) for name, record in book.data.items())


@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("The command is - add-birthday <name> <birthday>")
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday(birthday)

    return "Contact is updated"


@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("The command is - show-birthday <birthday>")
    name, *_ = args
    record = book.find(name)

    return str(record.birthday)


@input_error
def birthdays(book: AddressBook) -> str:
    congrats_list = book.get_upcoming_birthdays()
    if not congrats_list:
        return "No upcoming birthdays"
    return "\n".join(f"{c['name']}: {c['congratulation_date']}" for c in congrats_list)


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye! Saving your address book...")
            save_data(book)
            break
        elif command == "hello":
            print("""How can I help you? Commands:
                  add: adds contact to the address book
                  change: changes phone number
                  phone: shows phone number of a contact
                  all: lists all contacts in the address book
                  add-birthday: adds birthday to a contact
                  show-birthday: shows birthday of a contact
                  birthdays: lists upcoming birthdays""")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command")    


if __name__ == "__main__":
    main()
