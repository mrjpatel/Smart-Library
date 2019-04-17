class UserCredential:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_encrypted_password(self):
        # TODO: encrypt password
        return self.password
    
    @staticmethod
    def decrypt_password(cyphertext):
        # TODO: decrypt password
        return cyphertext
