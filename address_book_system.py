import re
from functools import wraps
from collections import defaultdict
import csv
import json

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
    
    def sort_by_name(self):
        return sorted(self.contacts, key=lambda c: (c.first_name.lower(), c.last_name.lower()))
    
    def sort_by_city(self):
        return sorted(self.contacts, key=lambda c: c.city.lower())

    def sort_by_state(self):
        return sorted(self.contacts, key=lambda c: c.state.lower())

    def sort_by_zip(self):
        return sorted(self.contacts, key=lambda c: c.zip_code)
    
    def export_to_txt(self, filename):
        with open(filename, 'w') as file:
            for contact in self.contacts:
                file.write(str(contact))
                file.write("\n" + "-" * 40 + "\n")
        print(f"Address book exported to plain text file: {filename}")
    
    def export_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["first_name", "last_name", "address", "city", "state", "zip_code", "phone_number", "email"])
            for c in self.contacts:
                writer.writerow([c.first_name, c.last_name, c.address, c.city, c.state, c.zip_code, c.phone_number, c.email])
        print(f"Address book exported to {filename} successfully.")

    def import_from_csv(self, filename):
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    contact = Contact(**row)
                    if contact not in self.contacts:
                        self.contacts.append(contact)
            print(f"Address book imported from {filename} successfully.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def export_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump([contact.__dict__ for contact in self.contacts], file, indent=4)
        print(f"Address book exported to {filename} successfully.")

    def import_from_json(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for entry in data:
                    contact = Contact(**entry)
                    if contact not in self.contacts:
                        self.contacts.append(contact)
            print(f"Address book imported from {filename} successfully.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

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
    
    def view_all_grouped_by_city(self):
        city_dict = defaultdict(list)
        for book_name, book in self.books.items():
            for contact in book.contacts:
                city_dict[contact.city].append((book_name, contact))
        return city_dict

    def view_all_grouped_by_state(self):
        state_dict = defaultdict(list)
        for book_name, book in self.books.items():
            for contact in book.contacts:
                state_dict[contact.state].append((book_name, contact))
        return state_dict
    
    def count_by_city(self):
        city_counts = defaultdict(int)
        for book in self.books.values():
            for contact in book.contacts:
                city_counts[contact.city] += 1
        return city_counts

    def count_by_state(self):
        state_counts = defaultdict(int)
        for book in self.books.values():
            for contact in book.contacts:
                state_counts[contact.state] += 1
        return state_counts

class AddressBookMain:
    def __init__(self):
        print("Welcome to Address Book Program")
