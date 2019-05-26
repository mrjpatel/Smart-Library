import hashlib

from .aes_cryptography import AESCryptography


class UserCredential:
    """
    Class used to store the user's credentials
    username: str
        The user's username
    password: str
        The user's password
    """
    def __init__(self, username, password):
        """
        :param username: the user's username
        :type username: str
        :param password: the user's password
        :type password: the user's password
        """
        self.username = username
        self.__hash = hashlib.sha256(password.encode()).hexdigest()
        self.cypher = AESCryptography()

    def get_encrypted_password(self):
        """
        Encrypts the user's hashed password
        :return: the cyphertext of the encrypted hashed password
        :rtype: byte
        """
        return self.cypher.encrypt(self.__hash)

    def is_compare_cyphertext(self, cyphertext):
        """
        Decrypts the cyphertext and checks whether
        it matches the hashed password
        :param cyphertext: the encrpyted cyphertext
        :type cyphertext: byte
        :return: true if the decrytped plain text matches the hashed password
        :rtype: bool
        """
        plaintext = self.cypher.decrypt(cyphertext)
        return self.__hash == plaintext
