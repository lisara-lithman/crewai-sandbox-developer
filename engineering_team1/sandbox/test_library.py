import unittest
from library import Library

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()

    def test_add_book(self):
        self.library.add_book('1984', 'George Orwell')
        self.assertEqual(len(self.library.catalog), 1)
        self.assertEqual(self.library.catalog[0].title, '1984')

    def test_borrow_book(self):
        self.library.add_book('1984', 'George Orwell')
        result = self.library.borrow_book('member1', '1984')
        self.assertEqual(result, 'Member member1 borrowed 1984.')
        self.assertFalse(self.library.catalog[0].availability)

    def test_return_book(self):
        self.library.add_book('1984', 'George Orwell')
        self.library.borrow_book('member1', '1984')
        result = self.library.return_book('member1', '1984')
        self.assertEqual(result, 'Member member1 returned 1984.')
        self.assertTrue(self.library.catalog[0].availability)

    def test_get_catalog(self):
        self.library.add_book('1984', 'George Orwell')
        catalog = self.library.get_catalog()
        self.assertEqual(len(catalog), 1)
        self.assertEqual(catalog[0]['title'], '1984')

    def test_is_book_available(self):
        self.library.add_book('1984', 'George Orwell')
        self.assertTrue(self.library.is_book_available('1984'))
        self.library.borrow_book('member1', '1984')
        self.assertFalse(self.library.is_book_available('1984'))

if __name__ == '__main__':
    unittest.main()