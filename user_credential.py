from aes_cryptography import AESCryptography


class UserCredential:
    def __init__(self, username, password):
        self.username = username
        self.__password = password
        self.cypher = AESCryptography()

    def get_encrypted_password(self):
        return self.cypher.encrypt(self.__password)

    def is_compare_cyphertext(self, cyphertext):
        plaintext = self.cypher.decrypt(cyphertext)
        return self.__password == plaintext
