import hashlib

from aes_cryptography import AESCryptography


class UserCredential:
    def __init__(self, username, password):
        self.username = username
        self.__hash = hashlib.sha256(password.encode()).hexdigest()
        self.cypher = AESCryptography()

    def get_encrypted_password(self):
        return self.cypher.encrypt(self.__hash)

    def is_compare_cyphertext(self, cyphertext):
        plaintext = self.cypher.decrypt(cyphertext)
        return self.__hash == plaintext
