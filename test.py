# test_use_case_1.py

from address_book_system import Contact

def test_create_contact():
    contact = Contact("Shriya", "Varnita", "123 Main St", "Chennai", "Tamil Nadu", "603203", "+91 9876543210", "shriyavarnita@example.com")
    assert contact.first_name == "Shriya"
    assert contact.last_name == "Varnita"
    assert "Shriya Varnita" in str(contact)
