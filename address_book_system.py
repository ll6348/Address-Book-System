class Contact:
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.email = email

    def __str__(self):
        return (f"Name       : {self.first_name} {self.last_name}\n"
                f"Address    : {self.address}, {self.city}, {self.state} - {self.zip_code}\n"
                f"Phone      : {self.phone_number}\n"
                f"Email      : {self.email}")