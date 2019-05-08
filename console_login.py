from menu_handler import MenuHandler
from user_credential import UserCredential

class ConsoleLogin(MenuHandler):
    def __init__(self, user_database):
        super().__init__(user_database)
        self.display_text = "Log in"

    def invoke(self):
        print("Log in to the LMS\n")
        username = self.get_username()
        password = self.get_password()
        credentials = UserCredential(username, password)
        user = self.validate_credentials(credentials)
        if user is None:
            print("Invalid credentials")
            return
        else:
            # TODO connect to master pi
            print("LOGGED IN")
            print(user)

    def validate_credentials(self, credentials):
        return self.db.get_user(credentials)

    def get_username(self):
        print("Username: ", end="")
        username = input().strip()
        return username
    
    def get_password(self):
        print("Password: ", end="")
        password = input().strip()
        return password
