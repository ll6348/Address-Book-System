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

@pytest.mark.usecase7
def test_prevent_duplicate_contact():
    ab = AddressBook()
    contact1 = Contact("Ravi", "Kumar", "Apt 1", "Chennai", "TN", "600001", "+91 9876543210", "ravi@example.com")
    contact2 = Contact("Ravi", "Kumar", "Another Addr", "City", "State", "123456", "+91 9123456789", "ravi2@example.com")

    added1 = ab.add_contact(contact1)
    added2 = ab.add_contact(contact2)

    assert added1 is True
    assert added2 is False  # duplicate name
    assert len(ab.contacts) == 1

@pytest.mark.usecase8
def test_search_by_city_and_state():
    system = AddressBookSystem()
    system.add_address_book("Friends")
    system.add_address_book("Work")

    friends = system.get_address_book("Friends")
    work = system.get_address_book("Work")

    friends.add_contact(Contact("Amit", "Shah", "123 Street", "Delhi", "Delhi", "110001", "+91 9999999999", "amit@example.com"))
    work.add_contact(Contact("Priya", "Singh", "456 Lane", "Delhi", "Haryana", "122001", "+91 8888888888", "priya@example.com"))

    city_results = system.search_by_city("Delhi")
    state_results = system.search_by_state("Haryana")

    assert len(city_results) == 2
    assert len(state_results) == 1
    assert city_results[0][0] == "Friends"
    assert state_results[0][0] == "Work"
