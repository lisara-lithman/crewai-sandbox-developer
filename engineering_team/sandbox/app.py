import gradio as gr
import pandas as pd

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
        member = next((m for m in self.members if m.member_id == member_id), None)
        if not member:
            member = Member(member_id, "Default User")
            self.members.append(member)

        book = next((b for b in self.books if b.title == book_title), None)
        if not book:
            return "Book not found."

        if not book.is_available:
            return "Book is not available."

        book.is_available = False
        member.borrowed_books.append(book)
        return "Book borrowed successfully."

    def return_book(self, member_id: str, book_title: str) -> str:
        member = next((m for m in self.members if m.member_id == member_id), None)
        if not member:
            return "Member not found."

        book = next((b for b in member.borrowed_books if b.title == book_title), None)
        if not book:
            return "This book was not borrowed by the member."

        book.is_available = True
        member.borrowed_books.remove(book)
        return "Book returned successfully."

    def get_catalog(self) -> pd.DataFrame:
        return pd.DataFrame([{ "Title": book.title, "Author": book.author, "Availability": book.is_available } for book in self.books])

    def get_member_info(self, member_id: str) -> dict:
        member = next((m for m in self.members if m.member_id == member_id), None)
        if not member:
            return {}
        return {
            "member_id": member.member_id,
            "name": member.name,
            "borrowed_books": [book.title for book in member.borrowed_books]
        }

library = Library()

def handle_add_book(title: str, author: str):
    library.add_book(title, author)
    return f"Book '{title}' added to catalog.", library.get_catalog()

def handle_borrow(member_id: str, book_title: str):
    msg = library.borrow_book(member_id, book_title)
    return msg, library.get_catalog()

def handle_return(member_id: str, book_title: str):
    msg = library.return_book(member_id, book_title)
    return msg, library.get_catalog()

app = gr.Blocks()

with app:
    gr.Markdown("# Smart Library System (Hierarchical Version)")
    with gr.Tab("Book Catalog View"):
        catalog_output = gr.Dataframe(value=library.get_catalog(), label="Book Catalog")

    with gr.Tab("Circulation"):
        with gr.Row():
            member_id_borrow = gr.Textbox(label="Member ID", placeholder="Enter Member ID")
            book_title_borrow = gr.Textbox(label="Book Title", placeholder="Enter Book Title")
            borrow_button = gr.Button("Borrow Book")
            borrow_output = gr.Textbox(label="Borrow Output")
            borrow_button.click(fn=handle_borrow, inputs=[member_id_borrow, book_title_borrow], outputs=[borrow_output, catalog_output])

        with gr.Row():
            member_id_return = gr.Textbox(label="Member ID", placeholder="Enter Member ID")
            book_title_return = gr.Textbox(label="Book Title", placeholder="Enter Book Title")
            return_button = gr.Button("Return Book")
            return_output = gr.Textbox(label="Return Output")
            return_button.click(fn=handle_return, inputs=[member_id_return, book_title_return], outputs=[return_output, catalog_output])

    with gr.Tab("Admin Actions"):
        title_input = gr.Textbox(label="Book Title", placeholder="Enter Book Title")
        author_input = gr.Textbox(label="Author", placeholder="Enter Author Name")
        add_button = gr.Button("Add Book")
        add_output = gr.Textbox(label="Add Book Output")
        add_button.click(fn=handle_add_book, inputs=[title_input, author_input], outputs=[add_output, catalog_output])

if __name__ == '__main__':
    app.launch()
