import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from library.reception.aes_cryptography import AESCryptography


class Test_AESCryptography(unittest.TestCase):
    def testEncryptPlainText(self):
        AESCryptography.get_secret_from_env = MagicMock(return_value=(
            bytes.fromhex(
                "F99F6E0098B54E3AE5EF2850EE68ACC532F87F17EE33F94B377E85C1002D6294"
            ),
            bytes.fromhex("798369938367EADD6C35E372C462F2E6")
        ))
        aes = AESCryptography()
        cyphertext = aes.encrypt("hello")
        expected = b'r\xe1\x07\xf9J\x15]FMa\x1e\xf8\xe4i\xfa\xa5z\x926_\xcf' \
                b'\xef7\xb7\xb9\xf7J\xed/Y>M'
        self.assertEqual(cyphertext, expected)

    def testDecryptCyphertext(self):
        cyphertext = b'r\xe1\x07\xf9J\x15]FMa\x1e\xf8\xe4i\xfa\xa5z\x926_\xcf' \
                b'\xef7\xb7\xb9\xf7J\xed/Y>M'

        AESCryptography.get_secret_from_env = MagicMock(return_value=(
            bytes.fromhex(
                "F99F6E0098B54E3AE5EF2850EE68ACC532F87F17EE33F94B377E85C1002D6294"
            ),
            bytes.fromhex("798369938367EADD6C35E372C462F2E6")
        ))
        aes = AESCryptography()
        plaintext = aes.decrypt(cyphertext)
        expected = "hello"
        self.assertEqual(plaintext, expected)


if __name__ == "__main__":
    unittest.main()
