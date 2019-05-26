import unittest
from unittest.mock import patch

from library.reception.console_login import ConsoleLogin


class Test_ConsoleLogin(unittest.TestCase):
    def test_valid_username(self):
        user_input = [
            "user1"
        ]
        with patch("builtins.input", side_effect=user_input):
            cl = ConsoleLogin("")
            username = cl.get_username()
            self.assertEqual(username, "user1")

    def test_valid_password(self):
        user_input = [
            "password123"
        ]
        with patch("builtins.input", side_effect=user_input):
            cl = ConsoleLogin("")
            username = cl.get_password()
            self.assertEqual(username, "user1")

if __name__ == "__main__":
    unittest.main()
