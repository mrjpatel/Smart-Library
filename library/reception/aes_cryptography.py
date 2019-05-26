import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


class AESCryptography:
    """
    This class is responsible for handling all AES cryptography operations.
    It is used to both encrypt and decrypt payloads.
    The AES 256 key and IV must be stored in environment variables:
        LMS_AES_256_KEY
        LMS_AES_256_IV
    """
    def __init__(self):
        secret = self.get_secret_from_env()
        self.__key = secret[0]
        self.__iv = secret[1]
        self.cypher = Cipher(
            algorithms.AES(self.__key),
            modes.CBC(self.__iv),
            backend=default_backend()
        )
        self.pad = PKCS7(256)

    @staticmethod
    def get_secret_from_env():
        """
        Retrieves the AES 256 key and IV from environment variables
            LMS_AES_256_KEY
            LMS_AES_256_IV
        :return: tuple containing the key and IV
        :rtype: tuple
        """
        env_key = os.environ["LMS_AES_256_KEY"]
        env_iv = os.environ["LMS_AES_256_IV"]
        return (bytes.fromhex(env_key), bytes.fromhex(env_iv))

    def encrypt(self, message):
        """
        Encrypts the message using the key and IV
        :param message: the message to encrypt
        :type message: str
        :return: the encrypted cyphertext
        :rtype: byte
        """
        encryptor = self.cypher.encryptor()
        padder = self.pad.padder()
        # message to bytes
        encoded_message = bytes(message, encoding="utf-8")
        # pad message to fit block size
        padded_message = padder.update(encoded_message) + padder.finalize()
        # encrypt message
        cyphertext = encryptor.update(padded_message) + encryptor.finalize()
        return cyphertext

    def decrypt(self, cyphertext):
        """
        Decrypts the cyphertext using the key and IV
        :param cyphertext: the cyphertext to decrypt
        :type cyphertext: byte
        :return: the decrypted plaintext
        :rtype: str
        """
        decryptor = self.cypher.decryptor()
        unpadder = self.pad.unpadder()
        # decrypt cyphertext
        plaintext = decryptor.update(cyphertext) + decryptor.finalize()
        # remove padding
        plaintext = unpadder.update(plaintext) + unpadder.finalize()
        return str(plaintext, encoding="utf-8")
