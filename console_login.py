from user_credential import UserCredential

class ConsoleLogin:
    def __init__(self, user_database):
        self.user_database = user_database

    def validate_credentials(self, credentials):
        # TODO: check credentials against database
        return True
