import json
import socket
import pickle
import subprocess

from library.common.menu_handler import MenuHandler
from .user_credential import UserCredential
from .qr_scanner import QrScanner
from .voice_search import VoiceSearch


class ConsoleLogin(MenuHandler):
    """
    Class for handling the console log in.
    It is used to to prompt the user for their credentials
    and attempting to authenitcate the user into the system

    user_database: str
        File path to the sqlite3 database
    """

    def __init__(self, user_database):
        """
        :param user_database: database for storing users on reception pi
        :type user_database: str
        """
        super().__init__(user_database)
        self.display_text = "Log in"

    def invoke(self):
        """
        Method that is called when the user selects the "Log in" option
        """
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
        """
        Validates the user's credentials against the database
        :param credentials: An object containing the user's credentials
        :type credentials: UserCredential
        :return: Whether the credentials are correct
        :rtype: bool
        """
        return self.db.get_user(credentials)

    def get_username(self):
        """
        Prompts and gets the username from the user
        """
        is_valid_username = False
        while not is_valid_username:
            print("Username: ", end="")
            username = input().strip()
            is_valid_username = username != ""
            if not is_valid_username:
                print("Please enter a username")
        return username

    def get_password(self):
        """
        Prompts and gets the password from the user
        """
        is_valid_password = False
        while not is_valid_password:
            print("Password: ", end="")
            password = input().strip()
            is_valid_password = password != ""
            if not is_valid_password:
                print("Please enter a password")
        return password

    def connect_to_master_pi(self, user):
        """
        Establishes a socket connection to the master pi
        :param user: The authenticated user
        :type user: dict
        """
        # get master pi ip and port from config
        with open("socket.json", "r") as f:
            config = json.load(f)
        ip = config["master_pi_ip"]
        port = config["port"]
        dest = (ip, port)

        # remove password from dict
        if "encrypted_password" in user:
            del user["encrypted_password"]

        # Connect to master pi
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to Master Pi on {}:{}...".format(*dest))
            s.connect(dest)
            serial_user = pickle.dumps(user)
            s.send(serial_user)
            print("Logging in as user {}".format(user["username"]))
            while True:
                message = s.recv(1024).decode("utf-8").strip()
                if message == "exit":
                    logout_message = s.recv(1024).decode("utf-8")
                    break
                if message == "barcode":
                    data = QrScanner.get_qr_codes()
                    print(data)
                    s.send(pickle.dumps(data))
                    print("Please continue on Master Pi")
                if message == "voice":
                    voice = VoiceSearch()
                    # clear screen of errors
                    subprocess.run("clear")
                    print("\nPrepare to speak")
                    search_term = voice.speech_to_text()
                    s.send(pickle.dumps(search_term))
                    print("Please continue on Master Pi")
            print(logout_message)
