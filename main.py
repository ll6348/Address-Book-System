from address_book_system import AddressBookSystem, AddressBookMain, Contact

def get_contact_from_console():
    print("\nEnter contact details:")
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

def select_address_book(system):
    name = input("Enter the name of the address book to use: ").strip()
    book = system.get_address_book(name)
    if not book:
        print("Address book not found. Would you like to create it?")
        if input("Create new address book? (y/n): ").strip().lower() == "y":
            try:
                system.add_address_book(name)
                print(f"Address book '{name}' created.")
                book = system.get_address_book(name)
            except ValueError as ve:
                print(str(ve))
    return book

if __name__ == "__main__":
    AddressBookMain()
    system = AddressBookSystem()

    while True:
        print("\nAddress Book System Menu:")
        print("1. Create New Address Book")
        print("2. Select Address Book")
        print("3. List All Address Books")
        print("4. Search by City")
        print("5. Search by State")
        print("6. View All Persons Grouped by City")
        print("7. View All Persons Grouped by State")
        print("8. Count Contacts by City")
        print("9. Count Contacts by State")
        print("10. Exit")

        main_choice = input("Choose an option: ").strip()

        if main_choice == "1":
            name = input("Enter a unique name for the address book: ").strip()
            try:
                system.add_address_book(name)
                print(f"Address book '{name}' created.")
            except ValueError as ve:
                print(str(ve))

        elif main_choice == "2":
            book = select_address_book(system)
            if not book:
                continue

            while True:
                print(f"\nAddress Book Menu ({name}):")
                print("1. Add Contact")
                print("2. Edit Contact by Name")
                print("3. Delete Contact by Name")
                print("4. List Contacts")
                print("5. Sort Contacts by Name")
                print("6. Sort Contacts by City")
                print("7. Sort Contacts by State")
                print("8. Sort Contacts by Zip Code")
                print("9. Export Address Book to Text File")
                print("10. Export Address Book to CSV")
                print("11. Import Address Book from CSV")
                print("12. Back to Main Menu")
                sub_choice = input("Choose an option: ").strip()

                if sub_choice == "1":
                    while True:
                        contact = get_contact_from_console()
                        success = book.add_contact(contact)
                        if success:
                            print("Contact added.")
                        else:
                            print("Duplicate contact. Skipped.")

                        cont = input("Add another contact? (y/n): ").strip().lower()
                        if cont != 'y':
                            break


                elif sub_choice == "2":
                    first = input("Enter First Name: ").strip()
                    last = input("Enter Last Name: ").strip()
                    updates = get_fields_to_update()
                    result = book.edit_contact_by_name(first, last, updates)
                    if result:
                        print("Contact updated successfully:")
                        print(result)
                    else:
                        print("Contact not found.")

                elif sub_choice == "3":
                    first = input("Enter First Name: ").strip()
                    last = input("Enter Last Name: ").strip()
                    deleted = book.delete_contact_by_name(first, last)
                    if deleted:
                        print("Contact deleted successfully.")
                    else:
                        print("Contact not found.")

                elif sub_choice == "4":
                    contacts = book.list_contacts()
                    if contacts:
                        for c in contacts:
                            print("\n" + c)
                    else:
                        print("No contacts found.")

                elif sub_choice == "5":
                    sorted_contacts = book.get_sorted_contacts()
                    if not sorted_contacts:
                        print("No contacts to display.")
                    else:
                        print("\nSorted Contacts:")
                        for contact in sorted_contacts:
                            print("\n" + str(contact))

                elif sub_choice == "6":
                    sorted_contacts = book.sort_by_city()
                    print("\nContacts Sorted by City:")
                    for c in sorted_contacts:
                        print("\n" + str(c))

                elif sub_choice == "7":
                    sorted_contacts = book.sort_by_state()
                    print("\nContacts Sorted by State:")
                    for c in sorted_contacts:
                        print("\n" + str(c))

                elif sub_choice == "8":
                    sorted_contacts = book.sort_by_zip()
                    print("\nContacts Sorted by Zip Code:")
                    for c in sorted_contacts:
                        print("\n" + str(c))

                elif sub_choice == "9":
                    filename = input("Enter text filename to export (e.g., book.txt): ").strip()
                    book.export_to_txt(filename)

                elif sub_choice == "10":
                    filename = input("Enter CSV filename to export (e.g., book.csv): ").strip()
                    book.export_to_csv(filename)

                elif sub_choice == "11":
                    filename = input("Enter CSV filename to import: ").strip()
                    book.import_from_csv(filename)
                    
                elif sub_choice == "12":
                    break

                else:
                    print("Invalid choice. Try again.")

        elif main_choice == "3":
            if not system.books:
                print("No address books created yet.")
            else:
                print("Address Books:")
                for bname in system.books.keys():
                    print(f"- {bname}")

        elif main_choice == "4":
            city = input("Enter city name to search: ").strip()
            results = system.search_by_city(city)
            if results:
                print(f"\nFound contacts in city '{city}':")
                for book_name, contact in results:
                    print(f"\n[Book: {book_name}]")
                    print(contact)
            else:
                print("No contacts found in this city.")

        elif main_choice == "5":
            state = input("Enter state name to search: ").strip()
            results = system.search_by_state(state)
            if results:
                print(f"\nFound contacts in state '{state}':")
                for book_name, contact in results:
                    print(f"\n[Book: {book_name}]")
                    print(contact)
            else:
                print("No contacts found in this state.")

        elif main_choice == "6":
            grouped = system.view_all_grouped_by_city()
            if not grouped:
                print("No contacts found.")
            else:
                for city, entries in grouped.items():
                    print(f"\nCity: {city}")
                    for book_name, contact in entries:
                        print(f"[Book: {book_name}] {contact}")

        elif main_choice == "7":
            grouped = system.view_all_grouped_by_state()
            if not grouped:
                print("No contacts found.")
            else:
                for state, entries in grouped.items():
                    print(f"\nState: {state}")
                    for book_name, contact in entries:
                        print(f"[Book: {book_name}] {contact}")

        elif main_choice == "8":
            city_counts = system.count_by_city()
            if not city_counts:
                print("No contacts available.")
            else:
                print("\nContact Count by City:")
                for city, count in city_counts.items():
                    print(f"{city}: {count} contact(s)")

        elif main_choice == "9":
            state_counts = system.count_by_state()
            if not state_counts:
                print("No contacts available.")
            else:
                print("\nContact Count by State:")
                for state, count in state_counts.items():
                    print(f"{state}: {count} contact(s)")

        elif main_choice == "10":
            print("Exiting Address Book Program.")
            break
        
        else:
            print("Invalid option. Try again.")
