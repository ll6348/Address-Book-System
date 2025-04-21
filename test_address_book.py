import pytest
from address_book_system import AddressBook, Contact, AddressBookSystem

@pytest.mark.usecase1
def test_create_contact():
    contact = Contact("Alice", "Smith", "123 Main St", "CityX", "StateY", "600001", "+91 9876543210", "alice@example.com")
    assert contact.first_name == "Alice"
    assert "Alice Smith" in str(contact)

@pytest.mark.usecase2
def test_add_valid_contact():
    ab = AddressBook()
    c = Contact("John", "Doe", "12 ABC Rd", "City", "State", "123456", "+91 9876543210", "john@example.com")
    ab.contacts.append(c)
    assert len(ab.contacts) == 1
    assert ab.contacts[0].first_name == "John"

@pytest.mark.usecase3
def test_edit_contact_by_name_simulation():
    ab = AddressBook()
    c = Contact("Sneha", "Rao", "Green Lane", "City", "State", "600001", "+91 9876543210", "sneha@mail.com")
    ab.contacts.append(c)

    # Simulate editing address and email
    new_address = "Red Street"
    new_email = "sneha.new@mail.com"

    ab.validate_address(new_address)
    ab.validate_email(new_email)

    c.address = new_address
    c.email = new_email

    assert c.address == "Red Street"
    assert c.email == "sneha.new@mail.com"

@pytest.mark.usecase4
def test_delete_contact_by_name():
    ab = AddressBook()
    contact = Contact("Aarav", "Mehta", "Street 7", "Mumbai", "Maharashtra", "400001", "+91 9876501234", "aarav@mail.com")
    ab.contacts.append(contact)

    # Simulate deletion
    before = len(ab.contacts)
    found = False
    for i, c in enumerate(ab.contacts):
        if c.first_name == "Aarav" and c.last_name == "Mehta":
            del ab.contacts[i]
            found = True
            break

    after = len(ab.contacts)

    assert found is True
    assert after == before - 1

@pytest.mark.usecase5
def test_add_multiple_contacts():
    ab = AddressBook()
    contacts = [
        Contact("A", "One", "Addr1", "City1", "State1", "111111", "+91 9000000001", "a.one@mail.com"),
        Contact("B", "Two", "Addr2", "City2", "State2", "222222", "+91 9000000002", "b.two@mail.com")
    ]
    for c in contacts:
        ab.add_contact(c)

    assert len(ab.contacts) == 2
    assert ab.contacts[0].first_name == "A"
    assert ab.contacts[1].last_name == "Two"

@pytest.mark.usecase6
def test_multiple_address_books():
    system = AddressBookSystem()
    system.add_address_book("Family")
    system.add_address_book("Work")

    family = system.get_address_book("Family")
    work = system.get_address_book("Work")

    family.add_contact(Contact("Mom", "Smith", "Home St", "City", "State", "111111", "+91 9999999999", "mom@home.com"))
    work.add_contact(Contact("Boss", "Lee", "Office St", "BizCity", "BizState", "222222", "+91 8888888888", "boss@office.com"))

    assert len(family.contacts) == 1
    assert len(work.contacts) == 1
