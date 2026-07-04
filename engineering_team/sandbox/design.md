# Design for Smart Library and Book Reservation System

## Overview
The system will be designed to manage a catalog of books within memory, allowing users to borrow and return books while providing an admin interface for managing the book catalog. The system will consist of backend logic to handle book management and user interactions, and a frontend using Gradio to display the information and allow user interactions through a multi-tab layout.

## Backend Design (Assigned to `backend_engineer`)

### Module: `library_system`

#### Class: `Book`
- **Attributes:**
  - `title: str`
  - `author: str`
  - `is_available: bool`
  
#### Class: `Member`
- **Attributes:**
  - `member_id: str`
  - `name: str`
  - `borrowed_books: List[Book]`
  
#### Class: `Library`
- **Attributes:**
  - `books: List[Book]`
  - `members: List[Member]`
  
- **Methods:**
  - `add_book(title: str, author: str) -> None`
  - `borrow_book(member_id: str, book_title: str) -> str`
  - `return_book(member_id: str, book_title: str) -> str`
  - `get_catalog() -> List[Dict[str, Union[str, bool]]]`
  - `get_member_info(member_id: str) -> Dict[str, Any]`

### Function Signatures:
```python
class Book:
    def __init__(self, title: str, author: str, is_available: bool = True):
        pass

class Member:
    def __init__(self, member_id: str, name: str):
        pass

class Library:
    def __init__(self):
        self.books = []
        self.members = []
    
    def add_book(self, title: str, author: str) -> None:
        pass

    def borrow_book(self, member_id: str, book_title: str) -> str:
        pass

    def return_book(self, member_id: str, book_title: str) -> str:
        pass

    def get_catalog(self) -> List[Dict[str, Union[str, bool]]]:
        pass

    def get_member_info(self, member_id: str) -> Dict[str, Any]:
        pass
```

## Frontend Design (Assigned to `frontend_engineer`)

### Gradio App Structure

#### Tabs:
1. **Tab 1: Book Catalog View**
   - Displays a dynamic table showing the complete list of books and their availability.
   - Refreshes automatically with actions performed in other tabs.

2. **Tab 2: Circulation**
   - **Borrow Book Form:**
     - Fields:
       - `member_id: str`
       - `book_title: str`
     - Button to execute `borrow_book()`.
  
   - **Return Book Form:**
     - Fields:
       - `member_id: str`
       - `book_title: str`
     - Button to execute `return_book()`.
  
3. **Tab 3: Admin Actions**
   - **Add Book Form:**
     - Fields:
       - `title: str`
       - `author: str`
     - Button to execute `add_book()`.

### Gradio Interface Signatures:
```python
import gradio as gr

def get_catalog() -> pd.DataFrame:
    pass

def borrow_book(member_id: str, book_title: str) -> str:
    pass

def return_book(member_id: str, book_title: str) -> str:
    pass

def add_book(title: str, author: str) -> None:
    pass

# Creating the Gradio interface with multiple tabs
app = gr.Blocks()
with app:
    with gr.Tab("Book Catalog View"):
        gr.Dataframe(get_catalog)
  
    with gr.Tab("Circulation"):
        with gr.Row():
            member_id_borrow = gr.Textbox(label="Member ID", placeholder="Enter Member ID")
            book_title_borrow = gr.Textbox(label="Book Title", placeholder="Enter Book Title")
            gr.Button("Borrow Book").click(borrow_book, inputs=[member_id_borrow, book_title_borrow])
 
        with gr.Row():
            member_id_return = gr.Textbox(label="Member ID", placeholder="Enter Member ID")
            book_title_return = gr.Textbox(label="Book Title", placeholder="Enter Book Title")
            gr.Button("Return Book").click(return_book, inputs=[member_id_return, book_title_return])
  
    with gr.Tab("Admin Actions"):
        title_input = gr.Textbox(label="Book Title")
        author_input = gr.Textbox(label="Author")
        gr.Button("Add Book").click(add_book, inputs=[title_input, author_input])
  
app.launch()
```

## Testing Design (Assigned to `test_engineer`)

### Module: `test_library_system`

#### Test Cases
- `test_add_book()`
  - Test adding a book to the catalog.
  
- `test_borrow_book()`
  - Test borrowing a book successfully.
  - Test borrowing a book that is already checked out.
  
- `test_return_book()`
  - Test returning a book successfully.
  - Test returning a book that was not borrowed.
  
- `test_get_catalog()`
  - Ensure it returns the correct structure with all current books.
  
- `test_get_member_info()`
  - Check if member information is retrieved correctly.

### Function Signatures for Tests
```python
def test_add_book():
    pass

def test_borrow_book():
    pass

def test_return_book():
    pass

def test_get_catalog():
    pass

def test_get_member_info():
    pass
```

This design outlines the necessary modules, classes, and functions to implement the smart library and book reservation system, with clear assignments for each engineer and detailed structures to adhere to the requirements provided.