from typing import List, Dict, Union

class Book:
    def __init__(self, title: str, author: str, availability: bool = True):
        self.title = title
        self.author = author
        self.availability = availability

class Library:
    def __init__(self):
        self.catalog: List[Book] = []
        self.members: Dict[str, List[Book]] = {}  # Maps member IDs to borrowed books

    def add_book(self, title: str, author: str) -> None:
        new_book = Book(title, author)
        self.catalog.append(new_book)

    def borrow_book(self, member_id: str, title: str) -> str:
        if not self.is_book_available(title):
            return f'Book {title} is not available for borrowing.'
        
        book_to_borrow = next((book for book in self.catalog if book.title == title), None)
        if book_to_borrow:
            if member_id not in self.members:
                self.members[member_id] = []
            self.members[member_id].append(book_to_borrow)
            book_to_borrow.availability = False
            return f'Member {member_id} borrowed {title}.'
        return 'Book not found in catalog.'

    def return_book(self, member_id: str, title: str) -> str:
        if member_id in self.members and title in [book.title for book in self.members[member_id]]:
            book_to_return = next((book for book in self.members[member_id] if book.title == title), None)
            if book_to_return:
                book_to_return.availability = True
                self.members[member_id].remove(book_to_return)
                return f'Member {member_id} returned {title}.'
        return 'This book was not borrowed by this member.'

    def get_catalog(self) -> List[Dict[str, Union[str, bool]]]:
        return [{'title': book.title, 'author': book.author, 'availability': book.availability} for book in self.catalog]

    def is_book_available(self, title: str) -> bool:
        return any(book.title == title and book.availability for book in self.catalog)