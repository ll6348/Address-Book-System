from address_book_system import AddressBook, AddressBookMain, Contact

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

def get_fields_to_update():
    fields = input("Enter field names to update (comma-separated): ").strip().lower().replace(" ", "").split(",")
    updates = {}
    for field in fields:
        value = input(f"Enter new value for {field.replace('_', ' ').title()}: ").strip()
        updates[field] = value
    return updates


if __name__ == "__main__":
    AddressBookMain()
    book = AddressBook()

    while True:
        print("\nOptions:")
        print("1. Add Contact")
        print("2. Edit Contact by Name")
        print("3. Delete Contact by Name")
        print("4. List Contacts")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            while True:
                contact = get_contact_from_console()
                book.add_contact(contact)
                print("Contact added.")

                cont = input("Do you want to add another contact? (y/n): ").strip().lower()
                if cont != 'y':
                    break

        elif choice == "2":
            first = input("Enter First Name: ").strip()
            last = input("Enter Last Name: ").strip()
            updates = get_fields_to_update()
            result = book.edit_contact_by_name(first, last, updates)
            if result:
                print("Contact updated successfully:")
                print(result)
            else:
                print("Contact not found.")

        elif choice == "3":
            first = input("Enter First Name: ").strip()
            last = input("Enter Last Name: ").strip()
            deleted = book.delete_contact_by_name(first, last)
            if deleted:
                print("Contact deleted successfully.")
            else:
                print("Contact not found.")

        elif choice == "4":
            for c in book.list_contacts():
                print("\n" + c)

        elif choice == "5":
            print("Exiting Address Book.")
            break

        else:
            print("Invalid choice. Try again.")
