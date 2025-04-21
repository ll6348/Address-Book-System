import pytest
from address_book_system import Contact

@pytest.mark.usecase1
def test_create_contact():
    contact = Contact("Alice", "Smith", "123 Main St", "CityX", "StateY", "600001", "+91 9876543210", "alice@example.com")
    assert contact.first_name == "Alice"
    assert "Alice Smith" in str(contact)
