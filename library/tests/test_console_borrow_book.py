import unittest
from unittest.mock import patch


from library.master.console_borrow_book import ConsoleBorrowBook
from library.common.lms_library_database import LMSLibraryDatabase


class Test_Console_Borrow_Book(unittest.TestCase):
    def test_is_borrowed(self):
        book = {
            "BookID": 1
        }
        user = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@gmail.com",
            "username": "jsmith"
        }
        test_db = "lms_library_config_test.json"
        cbb = ConsoleBorrowBook(test_db, user)
        self.assertFalse(cbb.is_borrowed)

if __name__ == "__main__":
    unittest.main()
