import unittest
from library_system import Library, Book, Member

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.member = Member("1", "John Doe")
        self.library.members.append(self.member)

    def test_add_book(self):
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald")
        catalog = self.library.get_catalog()
        self.assertEqual(len(catalog), 1)
        self.assertEqual(catalog[0]['title'], "The Great Gatsby")
        self.assertEqual(catalog[0]['author'], "F. Scott Fitzgerald")
        self.assertTrue(catalog[0]['is_available'])

    def test_borrow_book(self):
        self.library.add_book("1984", "George Orwell")
        self.assertEqual(self.library.borrow_book(self.member.member_id, "1984"), "Book borrowed successfully.")
        self.assertEqual(self.library.borrow_book(self.member.member_id, "1984"), "Book is not available.")

    def test_return_book(self):
        self.library.add_book("1984", "George Orwell")
        self.library.borrow_book(self.member.member_id, "1984")
        self.assertEqual(self.library.return_book(self.member.member_id, "1984"), "Book returned successfully.")
        self.assertEqual(self.library.return_book(self.member.member_id, "1984"), "This book was not borrowed by the member.")

    def test_get_catalog(self):
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald")
        self.library.add_book("1984", "George Orwell")
        catalog = self.library.get_catalog()
        self.assertEqual(len(catalog), 2)

    def test_get_member_info(self):
        info = self.library.get_member_info("1")
        self.assertEqual(info['name'], "John Doe")

if __name__ == '__main__':
    unittest.main()