import re

from user_credential import UserCredential
from menu_handler import MenuHandler


class ConsoleRegister(MenuHandler):
    def __init__(self, user_database):
        super().__init__(user_database)
        self.display_text = "Register"

    def invoke(self):
        print("Register an account\n")
        # get user details
        username = self.get_username()
        password = self.get_password()
        first_name = self.get_first_name()
        last_name = self.get_last_name()
        email = self.get_email()

        # create new user
        credentials = UserCredential(username, password)
        self.db.insert_user(credentials, first_name, last_name, email)
        print("Successfully registered!")

    def get_username(self):
        is_valid_username = False
        while not is_valid_username:
            print("Username: ", end="")
            username = input().strip()
            user_regex = re.compile("^\\w+$")
            is_valid_username = user_regex.match(username) is not None
            if not is_valid_username:
                print("{} is not a valid username".format(username))
            # check if username already exists in the system
            if self.db.is_username_exists(username):
                is_valid_username = False
                print("The username {} already exists".format(username))
        return username

    def get_password(self):
        is_valid_password = False
        while not is_valid_password:
            print("Password: ", end="")
            password = input().strip()
            pw_regex = re.compile("^\\w+$")
            is_valid_password = pw_regex.match(password) is not None
            if not is_valid_password:
                print("{} is not a valid password".format(password))
        return password

    def get_first_name(self):
        is_valid_first_name = False
        while not is_valid_first_name:
            print("First Name: ", end="")
            fname = input().strip()
            fn_regex = re.compile("^[A-Za-z]+$")
            is_valid_first_name = fn_regex.match(fname) is not None
            if not is_valid_first_name:
                print("{} is not a valid first name".format(fname))
        return fname

    def get_last_name(self):
        is_valid_last_name = False
        while not is_valid_last_name:
            print("Last Name: ", end="")
            lname = input().strip()
            ln_regex = re.compile("^[A-Za-z'-]+$")
            is_valid_last_name = ln_regex.match(lname) is not None
            if not is_valid_last_name:
                print("{} is not a valid last name".format(lname))
        return lname

    def get_email(self):
        is_valid_email = False
        while not is_valid_email:
            print("Email: ", end="")
            email = input().strip()
            email_regex = re.compile("^\\w+@([A-Za-z]\.)+[A-Za-z]$")
            is_valid_email = email_regex.match(email) is not None
            if not is_valid_email:
                print("{} is not a valid email".format(email))
        return email
