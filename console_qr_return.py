from datetime import datetime
from datetime import timedelta

from lms_library_database import LMSLibraryDatabase
from menu_handler import MenuHandler
from google_calander import GoogleCalanderAPI


class ConsoleReturnBook(MenuHandler):
    """
    A class to handle the customer borrowing a book

    max_borrow_days : int
        Number of days to borrow a book
    db : LMSLibraryDatabase
        Database object of the master database
    display_text : str
        Display test for the console menu
    user : dict
        User Object following the LMSLibraryDatabase.user_schema
    """
    max_borrow_days = 7

    def __init__(self, database, user):
        """
        :param database: Database Setting File location
        :type database: string
        :param user: User Object following the LMSLibraryDatabase.user_schema
        :type user: dict
        """
        self.db = LMSLibraryDatabase(database)
        self.display_text = "Return Book(s)"
        self.user = user

    def invoke(self):
        """
        Function that is called to invoke the return book function
        """
        exit = False
        while not exit:
            self.start()
            print("Return another book? (y/n): ", end="")
            str_input = input().strip()
            if str_input is not "y":
                exit = True