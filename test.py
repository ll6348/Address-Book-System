# test_use_case_1.py

from address_book_system import Contact

def test_create_contact():
    contact = Contact("Alice", "Smith", "123 Main St", "CityX", "StateY", "600001", "+91 9876543210", "alice@example.com")
    assert contact.first_name == "Alice"
    assert contact.last_name == "Smith"
    assert "Alice Smith" in str(contact)
