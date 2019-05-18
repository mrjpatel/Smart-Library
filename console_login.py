import socket
import pickle

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

        # authenticated, connect to master pi
        self.connect_to_master_pi(user)

    def validate_credentials(self, credentials):
        return self.db.get_user(credentials)

    def get_username(self):
        is_valid_username = False
        while not is_valid_username:
            print("Username: ", end="")
            username = input().strip()
            is_valid_username = username != ""
            if not is_valid_username:
                print("Please enter a username")
        return username
    
    def get_password(self):
        is_valid_password = False
        while not is_valid_password:
            print("Password: ", end="")
            password = input().strip()
            is_valid_password = password != ""
            if not is_valid_password:
                print("Please enter a password")
        return password

    def connect_to_master_pi(self, user):
        # TODO: remove hardcoded destination
        dest = ("localhost", 32674)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to Master Pi on {}:{}...".format(*dest))
            s.connect(dest)
            serial_user = pickle.dumps(user)
            s.send(serial_user)
            print("Logging in as user {}".format(user["username"]))
            logout_message = s.recv(1024)
            print(b"{}".format(logout_message))
