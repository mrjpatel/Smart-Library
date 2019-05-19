from datetime import datetime
from dateutil.parser import parse

from lms_library_database import LMSLibraryDatabase
from menu_handler import MenuHandler
from console_menu import ConsoleMenu
from prettytable import PrettyTable

class ConsoleBorrowBook(MenuHandler):

    def __init__(self, database, username):
        self.db = LMSLibraryDatabase(database)
        self.display_text = "Borrow Book(s)"
        self.user = username

    def invoke(self):
        print("\nEnter BookID to borrow: ", end="")
        # get option from user, and strip whitespace
        str_input = input().strip()
        # validate input
        if (not str_input.isdigit()):
            # input not a number
            print("{} is not a valid BookID".format(str_input))
            return
        # input is a number
        book_id = int(str_input)
        print("Book is: {}".format(self.is_borrowed(book_id)))
    
    def is_borrowed(book_id):
        # makes call to db to get borrowed record
        borrowed = db.query_borrowed_book(book_id)
        if not borrowed:
            return True
        else:
            return False

