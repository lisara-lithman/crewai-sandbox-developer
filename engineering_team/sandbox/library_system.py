from typing import List, Dict, Union, Any

class Book:
    def __init__(self, title: str, author: str, is_available: bool = True):
        self.title = title
        self.author = author
        self.is_available = is_available

class Member:
    def __init__(self, member_id: str, name: str):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, title: str, author: str) -> None:
        new_book = Book(title, author)
        self.books.append(new_book)

    def borrow_book(self, member_id: str, book_title: str) -> str:
        # Find the member
        member = next((m for m in self.members if m.member_id == member_id), None)
        if not member:
            return "Member not found."

        # Find the book
        book = next((b for b in self.books if b.title == book_title), None)
        if not book:
            return "Book not found."

        # Check availability
        if not book.is_available:
            return "Book is not available."

        # Borrow the book
        book.is_available = False
        member.borrowed_books.append(book)
        return "Book borrowed successfully."

    def return_book(self, member_id: str, book_title: str) -> str:
        # Find the member
        member = next((m for m in self.members if m.member_id == member_id), None)
        if not member:
            return "Member not found."

        # Find the book in borrowed books
        book = next((b for b in member.borrowed_books if b.title == book_title), None)
        if not book:
            return "This book was not borrowed by the member."

        # Return the book
        book.is_available = True
        member.borrowed_books.remove(book)
        return "Book returned successfully."

    def get_catalog(self) -> List[Dict[str, Union[str, bool]]]:
        return [{"title": book.title, "author": book.author, "is_available": book.is_available} for book in self.books]

    def get_member_info(self, member_id: str) -> Dict[str, Any]:
        member = next((m for m in self.members if m.member_id == member_id), None)
        if not member:
            return {}  # Member not found
        return {
            "member_id": member.member_id,
            "name": member.name,
            "borrowed_books": [book.title for book in member.borrowed_books]
        }