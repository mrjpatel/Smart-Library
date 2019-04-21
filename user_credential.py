class UserCredential:
    def __init__(self, username, password):
        self.username = username
        self.__password = password

    def get_encrypted_password(self):
        # TODO: encrypt password
        cyphetext = self.__password
        return cyphetext
    
    def is_compare_cyphertext(self, cyphertext):
        # TODO: set key
        plaintext = UserCredential.decrypt_password(cyphertext, "key")
        return self.__password == plaintext

    @staticmethod
    def decrypt_password(cyphertext, key):
        # TODO: decrypt password
        plaintext = cyphertext
        return plaintext
