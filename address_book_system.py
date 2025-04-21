from main import regex_validator

class Contact:
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.email = email

    def __str__(self):
        return (f"Name       : {self.first_name} {self.last_name}\n"
                f"Address    : {self.address}, {self.city}, {self.state} - {self.zip_code}\n"
                f"Phone      : {self.phone_number}\n"
                f"Email      : {self.email}")


class AddressBook:
    def __init__(self):
        self.contacts = []

    @regex_validator(r'^[A-Za-z]+$')
    def validate_first_name(self, name): return name

    @regex_validator(r'^[A-Za-z]+$')
    def validate_last_name(self, name): return name

    @regex_validator(r'^[A-Za-z0-9\s,/-]+$')
    def validate_address(self, address): return address

    @regex_validator(r'^[A-Za-z]+$')
    def validate_city(self, city): return city

    @regex_validator(r'^[A-Za-z\s]+$')
    def validate_state(self, state): return state

    @regex_validator(r'^\d{6}$')
    def validate_zip(self, zip_code): return zip_code

    @regex_validator(r'^\+91\s?\d{10}$')
    def validate_phone(self, phone): return phone

    @regex_validator(r'^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.[a-zA-Z]{2,}){1,2}$')
    def validate_email(self, email): return email

    def add_contact(self):
        from main import get_contact_from_console
        contact = get_contact_from_console()

        self.validate_first_name(contact.first_name)
        self.validate_last_name(contact.last_name)
        self.validate_address(contact.address)
        self.validate_city(contact.city)
        self.validate_state(contact.state)
        self.validate_zip(contact.zip_code)
        self.validate_phone(contact.phone_number)
        self.validate_email(contact.email)

        self.contacts.append(contact)
        print("\nContact added successfully!\n")
        print(contact)

    def list_contacts(self):
        return [str(c) for c in self.contacts]


class AddressBookSystem:
    def __init__(self):
        self.books = {}

    def add_address_book(self, name):
        if name in self.books:
            raise ValueError("Address Book with this name already exists.")
        self.books[name] = AddressBook()

    def get_address_book(self, name):
        return self.books.get(name)


class AddressBookMain:
    def __init__(self):
        print("Welcome to Address Book Program")
