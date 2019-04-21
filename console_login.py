from menu_handler import MenuHandler
from user_credential import UserCredential

class ConsoleLogin(MenuHandler):
    def __init__(self, user_database):
        super().__init__(user_database)
        self.display_text = "Log in"

    def invoke(self):
        # TODO: handle logging in
        print("LOGGING IN...")

    def validate_credentials(self, credentials):
        # TODO: check credentials against database
        return True
