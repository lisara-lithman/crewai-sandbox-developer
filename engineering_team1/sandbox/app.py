import gradio as gr
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

library = Library()

def update_catalog():
    return library.get_catalog()

def borrow_form(member_id: str, book_title: str):
    res = library.borrow_book(member_id, book_title)
    return res, library.get_catalog()

def return_form(member_id: str, book_title: str):
    res = library.return_book(member_id, book_title)
    return res, library.get_catalog()

def add_book_form(title: str, author: str):
    library.add_book(title, author)
    return f'Added {title} by {author} to the catalog.', library.get_catalog()

with gr.Blocks() as demo:
    gr.Markdown("# Smart Library System (Sequential Version)")

    with gr.Tab("Book Catalog View"):
        catalog_table = gr.Dataframe(update_catalog, label="Current Book Catalog")
    
    with gr.Tab("Circulation"):
        with gr.Row():
            member_id_input = gr.Textbox(label="Member ID")
            book_title_input = gr.Textbox(label="Book Title")
        borrow_button = gr.Button("Borrow Book")
        return_button = gr.Button("Return Book")
        borrow_output = gr.Textbox(label="Borrowing Result")
        return_output = gr.Textbox(label="Returning Result")
        borrow_button.click(borrow_form, [member_id_input, book_title_input], [borrow_output, catalog_table])
        return_button.click(return_form, [member_id_input, book_title_input], [return_output, catalog_table])
    
    with gr.Tab("Admin Actions"):
        with gr.Row():
            new_title_input = gr.Textbox(label="New Book Title")
            new_author_input = gr.Textbox(label="New Book Author")
        add_button = gr.Button("Add Book")
        add_output = gr.Textbox(label="Add Book Result")
        add_button.click(add_book_form, [new_title_input, new_author_input], [add_output, catalog_table])

if __name__ == '__main__':
    demo.launch()