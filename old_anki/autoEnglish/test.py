class Book:
    def __init__(self, isbn):
        self.isbn = isbn

class ComputerBook(Book):
    def __init__(self, name)