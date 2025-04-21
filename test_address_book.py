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

@pytest.mark.usecase9
def test_grouped_view_by_city_and_state():
    system = AddressBookSystem()
    system.add_address_book("Work")
    system.add_address_book("Family")

    work = system.get_address_book("Work")
    family = system.get_address_book("Family")

    c1 = Contact("Sam", "Roy", "123", "Delhi", "Delhi", "110001", "+91 9123456780", "sam@delhi.com")
    c2 = Contact("Lena", "Roy", "456", "Delhi", "UP", "110002", "+91 9123456781", "lena@delhi.com")
    c3 = Contact("Nina", "Patel", "789", "Mumbai", "MH", "400001", "+91 9123456782", "nina@mumbai.com")

    work.add_contact(c1)
    work.add_contact(c2)
    family.add_contact(c3)

    city_groups = system.view_all_grouped_by_city()
    state_groups = system.view_all_grouped_by_state()

    assert "Delhi" in city_groups
    assert "MH" in state_groups
    assert len(city_groups["Delhi"]) == 2
    assert len(state_groups["Delhi"]) == 1
    assert len(state_groups["UP"]) == 1

@pytest.mark.usecase10
def test_count_contacts_by_city_and_state():
    system = AddressBookSystem()
    system.add_address_book("A")
    system.add_address_book("B")

    a = system.get_address_book("A")
    b = system.get_address_book("B")

    a.add_contact(Contact("Anil", "Kumar", "Addr1", "Delhi", "Delhi", "123456", "+91 900001", "anil@mail.com"))
    b.add_contact(Contact("Sunita", "Mehra", "Addr2", "Delhi", "UP", "654321", "+91 900002", "sunita@mail.com"))
    b.add_contact(Contact("Ravi", "Sharma", "Addr3", "Mumbai", "MH", "400001", "+91 900003", "ravi@mail.com"))

    city_counts = system.count_by_city()
    state_counts = system.count_by_state()

    assert city_counts["Delhi"] == 2
    assert city_counts["Mumbai"] == 1
    assert state_counts["Delhi"] == 1
    assert state_counts["UP"] == 1
    assert state_counts["MH"] == 1

@pytest.mark.usecase11
def test_sort_contacts_by_name():
    ab = AddressBook()

    c1 = Contact("Zara", "Ali", "Addr1", "City", "State", "123456", "+91 900001", "zara@mail.com")
    c2 = Contact("Amit", "Bose", "Addr2", "City", "State", "654321", "+91 900002", "amit@mail.com")
    c3 = Contact("Amit", "Aaron", "Addr3", "City", "State", "111111", "+91 900003", "aaron@mail.com")

    ab.add_contact(c1)
    ab.add_contact(c2)
    ab.add_contact(c3)

    sorted_list = ab.get_sorted_contacts()
    names = [(c.first_name, c.last_name) for c in sorted_list]

    assert names == [("Amit", "Aaron"), ("Amit", "Bose"), ("Zara", "Ali")]

@pytest.mark.usecase12
def test_sort_by_city_state_zip():
    ab = AddressBook()

    ab.add_contact(Contact("John", "Doe", "123 St", "Mumbai", "MH", "400001", "+91 9000000001", "john@mail.com"))
    ab.add_contact(Contact("Jane", "Smith", "456 Ave", "Delhi", "DL", "110001", "+91 9000000002", "jane@mail.com"))
    ab.add_contact(Contact("Bob", "Lee", "789 Blvd", "Ahmedabad", "GJ", "380001", "+91 9000000003", "bob@mail.com"))

    by_city = [c.city for c in ab.sort_by_city()]
    by_state = [c.state for c in ab.sort_by_state()]
    by_zip = [c.zip_code for c in ab.sort_by_zip()]

    assert by_city == ["Ahmedabad", "Delhi", "Mumbai"]
    assert by_state == ["DL", "GJ", "MH"]
    assert by_zip == ["110001", "380001", "400001"]

@pytest.mark.usecase13
def test_export_to_text(tmp_path):
    ab = AddressBook()
    contact = Contact("Maya", "Iyer", "222 Road", "Pune", "MH", "411001", "+91 9000000009", "maya@mail.com")
    ab.add_contact(contact)

    file_path = tmp_path / "book.txt"
    ab.export_to_txt(file_path)

    content = file_path.read_text()
    assert "Maya Iyer" in content
    assert "222 Road" in content
    assert "Phone" in content

@pytest.mark.usecase14
def test_csv_export_and_import(tmp_path):
    book = AddressBook()
    contact = Contact("Arya", "Sharma", "101 Block", "Bangalore", "KA", "560001", "+91 9111222233", "arya@mail.com")
    book.add_contact(contact)

    csv_file = tmp_path / "contacts.csv"
    book.export_to_csv(csv_file)

    # Load into another address book
    new_book = AddressBook()
    new_book.import_from_csv(csv_file)

    assert len(new_book.contacts) == 1
    assert new_book.contacts[0].first_name == "Arya"
    assert new_book.contacts[0].email == "arya@mail.com"

@pytest.mark.usecase15
def test_json_export_and_import(tmp_path):
    book = AddressBook()
    contact = Contact("Kunal", "Verma", "5th Avenue", "Lucknow", "UP", "226001", "+91 9998887776", "kunal@mail.com")
    book.add_contact(contact)

    json_file = tmp_path / "contacts.json"
    book.export_to_json(json_file)

    # Load into another book
    new_book = AddressBook()
    new_book.import_from_json(json_file)

    assert len(new_book.contacts) == 1
    assert new_book.contacts[0].first_name == "Kunal"
    assert new_book.contacts[0].city == "Lucknow"
