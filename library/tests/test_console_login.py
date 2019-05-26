import unittest
from unittest.mock import patch

from library.reception.console_login import ConsoleLogin


class Test_ConsoleLogin(unittest.TestCase):
    def testValidateUsername(self):
        with patch("builtins.input", side_effect="user1"):
            cl = ConsoleLogin("")
            username = cl.get_username()
            self.assertEqual(username, "user1")


if __name__ == "__main__":
    unittest.main()
