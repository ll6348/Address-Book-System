# main.py
import re
from functools import wraps
from address_book_system import Contact

def regex_validator(pattern):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not re.fullmatch(pattern, value):
                raise ValueError(f"Invalid value for {func.__name__}: {value}")
            return func(self, value)
        return wrapper
    return decorator


def get_contact_from_console():
    print("Enter contact details:")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    address = input("Address: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    zip_code = input("ZIP Code: ").strip()
    phone_number = input("Phone Number (+91 1234567890): ").strip()
    email = input("Email: ").strip()

    return Contact(first_name, last_name, address, city, state, zip_code, phone_number, email)
