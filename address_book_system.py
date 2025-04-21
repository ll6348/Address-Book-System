import re
from functools import wraps

def regex_validator(pattern):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not re.fullmatch(pattern, value):
                raise ValueError(f"Invalid value for {func.__name__}: {value}")
            return func(self, value)
        return wrapper
    return decorator


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

    def __eq__(self, other):
        if isinstance(other, Contact):
            return (self.first_name.lower() == other.first_name.lower() and
                    self.last_name.lower() == other.last_name.lower())
        return False

    def __hash__(self):
        return hash((self.first_name.lower(), self.last_name.lower()))

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

    def add_contact(self, contact):
        self.validate_first_name(contact.first_name)
        self.validate_last_name(contact.last_name)
        self.validate_address(contact.address)
        self.validate_city(contact.city)
        self.validate_state(contact.state)
        self.validate_zip(contact.zip_code)
        self.validate_phone(contact.phone_number)
        self.validate_email(contact.email)

        if contact in self.contacts:
            print("Duplicate contact! Cannot add.")
            return False

        self.contacts.append(contact)
        return True

    def list_contacts(self):
        return [str(c) for c in self.contacts]

    def edit_contact_by_name(self, first_name, last_name, updates: dict):
        for contact in self.contacts:
            if contact.first_name.lower() == first_name.lower() and contact.last_name.lower() == last_name.lower():
                for field, new_value in updates.items():
                    if field == "first_name":
                        self.validate_first_name(new_value)
                    elif field == "last_name":
                        self.validate_last_name(new_value)
                    elif field == "address":
                        self.validate_address(new_value)
                    elif field == "city":
                        self.validate_city(new_value)
                    elif field == "state":
                        self.validate_state(new_value)
                    elif field == "zip_code":
                        self.validate_zip(new_value)
                    elif field == "phone_number":
                        self.validate_phone(new_value)
                    elif field == "email":
                        self.validate_email(new_value)
                    else:
                        continue  # Skip invalid field names

                    setattr(contact, field, new_value)
                return contact
        return None

    def delete_contact_by_name(self, first_name, last_name):
        for i, contact in enumerate(self.contacts):
            if contact.first_name.lower() == first_name.lower() and contact.last_name.lower() == last_name.lower():
                return self.contacts.pop(i)
        return None


class AddressBookSystem:
    def __init__(self):
        self.books = {}

    def add_address_book(self, name):
        if name in self.books:
            raise ValueError("Address Book with this name already exists.")
        self.books[name] = AddressBook()

    def get_address_book(self, name):
        return self.books.get(name)
    
    def search_by_city(self, city):
        results = []
        for book_name, book in self.books.items():
            for contact in book.contacts:
                if contact.city.lower() == city.lower():
                    results.append((book_name, contact))
        return results

    def search_by_state(self, state):
        results = []
        for book_name, book in self.books.items():
            for contact in book.contacts:
                if contact.state.lower() == state.lower():
                    results.append((book_name, contact))
        return results


class AddressBookMain:
    def __init__(self):
        print("Welcome to Address Book Program")
