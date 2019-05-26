import re

from library.common.menu_handler import MenuHandler
from .user_credential import UserCredential
from .face_registration import FaceRegistration
from image_encoding import ImageEncoding


class ConsoleRegister(MenuHandler):
    """
    Class to handle the text based user registration through the console
    user_database: str
        The location of the user database
    """
    def __init__(self, user_database):
        """
        :param user_database: The location of the user database
        :type user_database: str
        """
        super().__init__(user_database)
        self.display_text = "Register"

    def invoke(self):
        """
        Method to invoke the handler if the user selects the register option
        """
        print("Register an account\n")
        # get user details
        username = self.get_username()
        password = self.get_password()
        first_name = self.get_first_name()
        last_name = self.get_last_name()
        email = self.get_email()
        self.register_face(username)

        # create new user
        credentials = UserCredential(username, password)
        self.db.insert_user(credentials, first_name, last_name, email)
        print("Successfully registered!")

    def get_username(self):
        """
        Prompt and gets the username from the user
        :return: The inputted username
        :rtype: str
        """
        is_valid_username = False
        while not is_valid_username:
            print("Username: ", end="")
            username = input().strip()
            user_regex = re.compile(r"^\w+$")
            is_valid_username = user_regex.match(username) is not None
            if not is_valid_username:
                print("{} is not a valid username".format(username))
            # check if username already exists in the system
            if self.db.is_username_exists(username):
                is_valid_username = False
                print("The username {} already exists".format(username))
        return username

    def get_password(self):
        """
        Prompt and get the password from the user
        :return: The inputted password
        :rtype: str
        """
        is_valid_password = False
        while not is_valid_password:
            print("Password: ", end="")
            password = input().strip()
            pw_regex = re.compile(r"^\w+$")
            is_valid_password = pw_regex.match(password) is not None
            if not is_valid_password:
                print("{} is not a valid password".format(password))
        return password

    def get_first_name(self):
        """
        Prompt and get the first name from the user
        :return: the inputted first name
        :rtype: str
        """
        is_valid_first_name = False
        while not is_valid_first_name:
            print("First Name: ", end="")
            fname = input().strip()
            fn_regex = re.compile(r"^[A-Za-z]+$")
            is_valid_first_name = fn_regex.match(fname) is not None
            if not is_valid_first_name:
                print("{} is not a valid first name".format(fname))
        return fname

    def get_last_name(self):
        """
        Prompt and get the last name from the user
        :return: the inputted last name
        :rtype: str
        """
        is_valid_last_name = False
        while not is_valid_last_name:
            print("Last Name: ", end="")
            lname = input().strip()
            ln_regex = re.compile(r"^[A-Za-z'-]+$")
            is_valid_last_name = ln_regex.match(lname) is not None
            if not is_valid_last_name:
                print("{} is not a valid last name".format(lname))
        return lname

    def get_email(self):
        """
        Prompt and get the email from the user
        :return: the inputted email
        :rtype: str
        """
        is_valid_email = False
        while not is_valid_email:
            print("Email: ", end="")
            email = input().strip()
            email_regex_str = r"""
                ([!#-'*+/-9=?A-Z^-~-]+(\.[!#-'*+/-9=?A-Z^-~-]+)*
                |"([]!#-[^-~ \t]|(\\[\t -~]))+")@
                ([!#-'*+/-9=?A-Z^-~-]+(\.[!#-'*+/-9=?A-Z^-~-]+)*
                |\[[\t -Z^-~]*])"""
            email_regex = re.compile(email_regex_str)
            is_valid_email = email_regex.match(email) is not None
            if not is_valid_email:
                print("{} is not a valid email".format(email))
        return email

    def register_face(self, username):
        """
        Prompt and get the toogle to register face
        :param username: The username of user
        :type username: str
        """
        print("Please wait to register your face")

        face_register = FaceRegistration()
        face_registered = face_register.register(username)

        image_encode = ImageEncoding()
        image_encode.encode("encodings.pickle")

