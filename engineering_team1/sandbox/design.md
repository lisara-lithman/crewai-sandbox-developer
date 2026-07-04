```markdown
# Design Document for Smart Library and Book Reservation System

## Overview
This document outlines the design for a smart library and book reservation system. The system will allow users to manage books in memory without persistent storage and includes features for borrowing, returning books, and administering the book catalog. The UI will be built using Gradio, providing a clean multi-tab layout.

## Modules and Classes

### Backend Module
**Class: Book**
- Attributes:
  - `title: str`
  - `author: str`
  - `availability: bool`
  
**Class: Library**
- Attributes:
  - `catalog: List[Book]`
  - `members: Dict[str, List[Book]]`  # Maps member IDs to borrowed books
- Methods:
  - `add_book(title: str, author: str) -> None`
  - `borrow_book(member_id: str, title: str) -> str`
  - `return_book(member_id: str, title: str) -> str`
  - `get_catalog() -> List[Dict[str, Union[str, bool]]]`  # Returns a list of books with titles and availability
  - `is_book_available(title: str) -> bool`

**Engineer Assignment: backend_engineer**

### Frontend Module
- **Gradio Interface**
  
**Function: create_ui() -> None**
- Sets up the Gradio interface with 3 tabs:
    - **Tab 1: Book Catalog View**
        - Displays the book catalog as a Dynamic DataFrame
        - Function signature: `update_catalog() -> List[Dict[str, Union[str, bool]]]`
  
    - **Tab 2: Circulation**
        - **Borrow Form**
            - Function signature: `borrow_form(member_id: str, book_title: str) -> str`
        - **Return Form**
            - Function signature: `return_form(member_id: str, book_title: str) -> str`
  
    - **Tab 3: Admin Actions**
        - **Add Book Form**
            - Function signature: `add_book_form(title: str, author: str) -> str`

**Engineer Assignment: frontend_engineer**

### Testing Module
- **Unit Tests for Backend Functions**

**Class: TestLibrary**
- Methods:
  - `test_add_book() -> None`
  - `test_borrow_book() -> None`
  - `test_return_book() -> None`
  - `test_get_catalog() -> None`
  - `test_is_book_available() -> None`

**Engineer Assignment: test_engineer**

---

## High-Level Flow of Operation

1. The `backend_engineer` will implement the `Book` and `Library` classes along with their respective methods to handle books in memory.
2. The `frontend_engineer` will develop a Gradio application that includes three tabs, iterating functionalities to interact with the backend through defined signatures.
3. The `test_engineer` will focus on writing comprehensive unit tests for the allocated backend methods ensuring robustness.

## Conclusion
The design meets the requirements provided, ensuring a clean and interactive system that manages book reservations seamlessly without persistent storage. The division of work between engineers promotes effective collaboration in the sandbox environment.
```