class SomeError(Exception):
    def __init__(self, phone):
        self.phone = phone

    def __str__(self):
        return f"Trouble with phone number: {self.phone}"
