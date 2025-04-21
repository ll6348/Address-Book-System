import re
import csv
import json
from functools import wraps
from collections import defaultdict
from pydantic import BaseModel, EmailStr, field_validator

class Contact(BaseModel):
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone_number: str
    email: EmailStr

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v):
        if not v.isalpha():
            raise ValueError("Name must contain only alphabetic characters.")
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v):
        import re
        if not re.fullmatch(r'^[A-Za-z0-9\s,/-]+$', v):
            raise ValueError("Address must be alphanumeric and may include , / -")
        return v

    @field_validator("city")
    @classmethod
    def validate_city(cls, v):
        if not v.isalpha():
            raise ValueError("City must contain only letters.")
        return v

    @field_validator("state")
    @classmethod
    def validate_state(cls, v):
        if not all(x.isalpha() or x.isspace() for x in v):
            raise ValueError("State must contain only letters and spaces.")
        return v

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, v):
        if not v.isdigit() or len(v) != 6:
            raise ValueError("ZIP code must be 6 digits.")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        import re
        if not re.fullmatch(r'^\+91\s?\d{10}$', v):
            raise ValueError("Phone number must be in the format +91 1234567890.")
        return v

    def __str__(self):
        return (
            f"Name       : {self.first_name} {self.last_name}\n"
            f"Address    : {self.address}, {self.city}, {self.state} - {self.zip_code}\n"
            f"Phone      : {self.phone_number}\n"
            f"Email      : {self.email}"
        )

    def __eq__(self, other):
        """
        Checks if two Contact objects are equal based on their first and last name.

        Args:
            other (Contact): The other contact to compare with.

        Returns:
            bool: True if the contacts have the same first and last name, otherwise False.
        """
        if isinstance(other, Contact):
            return (self.first_name.lower() == other.first_name.lower() and
                    self.last_name.lower() == other.last_name.lower())
        return False

    def __hash__(self):
        """
        Generates a hash value for the Contact object based on the first and last name.

        Returns:
            int: The hash value for the contact.
        """
        return hash((self.first_name.lower(), self.last_name.lower()))

    def __str__(self):
        """
        Returns a string representation of the Contact object.

        Returns:
            str: A formatted string with contact details.
        """
        return (
            f"Name       : {self.first_name} {self.last_name}\n"
            f"Address    : {self.address}, {self.city}, {self.state} - {self.zip_code}\n"
            f"Phone      : {self.phone_number}\n"
            f"Email      : {self.email}"
        )


class AddressBook:
    """
    A class that manages a collection of contacts, allowing addition, editing, deletion, 
    and listing of contacts, along with support for validation, sorting, and file I/O operations.

    Attributes:
        contacts (list): A list of Contact objects stored in the address book.
    """

    def __init__(self):
        """
        Initializes an empty address book to store contacts.

        Attributes:
            contacts (list): A list to store the contacts in the address book.
        """
        self.contacts = []

    def add_contact(self, contact):
        """
        Add a contact to the address book after validation.

        Args:
            contact (Contact): The contact to add.

        Returns:
            bool: True if contact is added successfully, False if it's a duplicate.
        """

        if contact in self.contacts:
            print("Duplicate contact! Cannot add.")
            return False

        self.contacts.append(contact)
        return True

    def list_contacts(self):
        """
        List all contacts in the address book.

        Returns:
            list: A list of string representations of all contacts.
        """
        return [str(c) for c in self.contacts]

    def edit_contact_by_name(self, first_name, last_name, updates: dict):
        """
        Edit a contact's details by their first and last name.

        Args:
            first_name (str): The first name of the contact to edit.
            last_name (str): The last name of the contact to edit.
            updates (dict): A dictionary of fields to update with their new values.

        Returns:
            Contact or None: The updated contact if found, otherwise None.
        """
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
                        continue
                    setattr(contact, field, new_value)
                return contact
        return None

    def delete_contact_by_name(self, first_name, last_name):
        """
        Delete a contact by their first and last name.

        Args:
            first_name (str): The first name of the contact to delete.
            last_name (str): The last name of the contact to delete.

        Returns:
            Contact or None: The deleted contact if found, otherwise None.
        """
        for i, contact in enumerate(self.contacts):
            if contact.first_name.lower() == first_name.lower() and contact.last_name.lower() == last_name.lower():
                return self.contacts.pop(i)
        return None

    # Sorting
    def sort_by_name(self):
        """
        Sort contacts by their full name (first name then last name).

        Returns:
            list: A sorted list of contacts by name.
        """
        return sorted(self.contacts, key=lambda c: (c.first_name.lower(), c.last_name.lower()))

    def sort_by_city(self):
        """
        Sort contacts by their city.

        Returns:
            list: A sorted list of contacts by city.
        """
        return sorted(self.contacts, key=lambda c: c.city.lower())

    def sort_by_state(self):
        """
        Sort contacts by their state.

        Returns:
            list: A sorted list of contacts by state.
        """
        return sorted(self.contacts, key=lambda c: c.state.lower())

    def sort_by_zip(self):
        """
        Sort contacts by their zip code.

        Returns:
            list: A sorted list of contacts by zip code.
        """
        return sorted(self.contacts, key=lambda c: c.zip_code)

    # File I/O: TXT
    def export_all_to_txt(self, filename):
        """
        Exports all address books and their contacts to a text file.
    
        Args:
            filename (str): The name of the file where address books will be exported.
        """
        with open(filename, 'w') as file:
            for book_name, book in self.books.items():
                file.write(f"--- Address Book: {book_name} ---\n")
                for contact in book.contacts:
                    file.write(str(contact))
                    file.write("\n" + "-" * 40 + "\n")
                file.write("\n")
        print(f"All address books exported to {filename} successfully.")
    
    def import_all_from_txt(self, filename):
        """
        Imports all address books and their contacts from a text file.
    
        Args:
            filename (str): The name of the file to import address books from.
        """
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            current_book = None
            contact_lines = []

            for line in lines:
                line = line.strip()

                if line.startswith("--- Address Book:"):
                    current_book = line.split(":", 1)[1].strip().strip(" -")
                    if current_book not in self.books:
                        self.add_address_book(current_book)

                elif line.startswith("Name"):
                    contact_lines = lines[lines.index(line):lines.index(line)+4]
                    name = contact_lines[0].split(":", 1)[1].strip()
                    address = contact_lines[1].split(":", 1)[1].strip()
                    phone = contact_lines[2].split(":", 1)[1].strip()
                    email = contact_lines[3].split(":", 1)[1].strip()

                    first_name, last_name = name.split(" ", 1)
                    addr_parts = address.split(", ")
                    address = addr_parts[0]
                    city = addr_parts[1]
                    state, zip_code = addr_parts[2].split(" - ")

                    contact = Contact(
                        first_name, last_name, address,
                        city, state, zip_code, phone, email
                    )

                    if contact not in self.books[current_book].contacts:
                        self.books[current_book].contacts.append(contact)

            print(f"All address books imported from '{filename}' successfully.")

        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error while reading file: {e}")

    # File I/O: CSV
    def export_to_csv(self, filename):
        """
        Exports the current address book contacts to a CSV file.
    
        Args:
            filename (str): The name of the file to export the address book to.
        """
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["first_name", "last_name", "address", "city", "state", "zip_code", "phone_number", "email"])
            for c in self.contacts:
                writer.writerow([c.first_name, c.last_name, c.address, c.city, c.state,
                                 c.zip_code, c.phone_number, c.email])
        print(f"Address book exported to {filename} successfully.")

    def import_from_csv(self, filename):
        """
        Imports contacts from a CSV file into the current address book.
        
        Args:
            filename (str): The name of the file to import contacts from.
        """
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

    # File I/O: JSON
    def export_to_json(self, filename):
        """
        Exports the current address book contacts to a JSON file.
        
        Args:
            filename (str): The name of the file to export the address book to.
        """
        with open(filename, 'w') as file:
            json.dump([c.model_dump() for c in self.contacts], file, indent=4)
        print(f"Address book exported to {filename} successfully.")

    def import_from_json(self, filename):
        """
        Imports contacts from a JSON file into the current address book.
    
        Args:
            filename (str): The name of the file to import contacts from.
        """
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
    """
    Manages a collection of uniquely named address books.
    Supports global operations across books such as search, view, and count
    by city and state.
    """

    def __init__(self):
        """
        Initializes the address book system with an empty dictionary of books.
        """
        self.books = {}

    def add_address_book(self, name):
        """
        Adds a new address book with the specified unique name.

        Parameters:
            name (str): The name of the new address book.

        Raises:
            ValueError: If an address book with the given name already exists.
        """
        if name in self.books:
            raise ValueError("Address Book with this name already exists.")
        self.books[name] = AddressBook()

    def get_address_book(self, name):
        """
        Retrieves an address book by name.

        Parameters:
            name (str): The name of the address book.

        Returns:
            AddressBook or None: The corresponding address book, or None if not found.
        """
        return self.books.get(name)

    def search_by_city(self, city):
        """
        Searches all address books for contacts in a specific city.

        Parameters:
            city (str): The city name to search for.

        Returns:
            list: A list of tuples (book_name, contact) for matches.
        """
        results = []
        for book_name, book in self.books.items():
            for contact in book.contacts:
                if contact.city.lower() == city.lower():
                    results.append((book_name, contact))
        return results

    def search_by_state(self, state):
        """
        Searches all address books for contacts in a specific state.

        Parameters:
            state (str): The state name to search for.

        Returns:
            list: A list of tuples (book_name, contact) for matches.
        """
        results = []
        for book_name, book in self.books.items():
            for contact in book.contacts:
                if contact.state.lower() == state.lower():
                    results.append((book_name, contact))
        return results

    def view_all_grouped_by_city(self):
        """
        Groups all contacts across books by city.

        Returns:
            dict: A dictionary mapping each city to a list of (book_name, contact) tuples.
        """
        city_dict = defaultdict(list)
        for book_name, book in self.books.items():
            for contact in book.contacts:
                city_dict[contact.city].append((book_name, contact))
        return city_dict

    def view_all_grouped_by_state(self):
        """
        Groups all contacts across books by state.

        Returns:
            dict: A dictionary mapping each state to a list of (book_name, contact) tuples.
        """
        state_dict = defaultdict(list)
        for book_name, book in self.books.items():
            for contact in book.contacts:
                state_dict[contact.state].append((book_name, contact))
        return state_dict

    def count_by_city(self):
        """
        Counts the number of contacts in each city across all address books.

        Returns:
            dict: A dictionary mapping city names to their contact count.
        """
        city_counts = defaultdict(int)
        for book in self.books.values():
            for contact in book.contacts:
                city_counts[contact.city] += 1
        return city_counts

    def count_by_state(self):
        """
        Counts the number of contacts in each state across all address books.

        Returns:
            dict: A dictionary mapping state names to their contact count.
        """
        state_counts = defaultdict(int)
        for book in self.books.values():
            for contact in book.contacts:
                state_counts[contact.state] += 1
        return state_counts


class AddressBookMain:
    """
    Entry point class that displays a welcome message
    when the Address Book program starts.
    """

    def __init__(self):
        """
        Prints a welcome message to the user.
        """
        print("Welcome to Address Book Program")
