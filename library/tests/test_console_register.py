import unittest
from unittest.mock import patch

from library.reception.console_register import ConsoleRegister


class Test_ConsoleRegister(unittest.TestCase):
    def test_valid_password(self):
        user_input = [
            "password123"
        ]
        with patch("builtins.input", side_effect=user_input):
            cr = ConsoleRegister("")
            password = cr.get_password()
            self.assertEqual(password, "password123")
        
    def test_valid_first_name(self):
        user_input = [
            "John"
        ]
        with patch("builtins.input", side_effect=user_input):
            cr = ConsoleRegister("")
            first_name = cr.get_first_name()
            self.assertEqual(first_name, "John")
    
    def test_valid_last_name(self):
        user_input = [
            "Smith"
        ]
        with patch("builtins.input", side_effect=user_input):
            cr = ConsoleRegister("")
            last_name = cr.get_last_name()
            self.assertEqual(last_name, "Smith")
    
    def test_valid_email(self):
        user_input = [
            "test@example.com"
        ]
        with patch("builtins.input", side_effect=user_input):
            cr = ConsoleRegister("")
            email = cr.get_email()
            self.assertEqual(email, "test@example.com")


if __name__ == "__main__":
    unittest.main()
