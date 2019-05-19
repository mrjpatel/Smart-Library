from datetime import datetime
from datetime import timedelta

from lms_library_database import LMSLibraryDatabase
from menu_handler import MenuHandler
from console_menu import ConsoleMenu
from prettytable import PrettyTable

class ConsoleBorrowBook(MenuHandler):
    max_borrow_days = 7

    def __init__(self, database, username):
        self.db = LMSLibraryDatabase(database)
        self.display_text = "Borrow Book(s)"
        self.username = username

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
        # check if book exists
        if not self.db.query_book_by_id(book_id):
            print("Book with ID {} does not exist!".format(book_id))
            return
        # check if book is borrowed
        if self.is_borrowed(book_id):
            print("Book with ID {} is currently borrowed!".format(book_id))
            return
        self.borrow_book(book_id)
    
    def is_borrowed(self, book_id):
        # makes call to db to get borrowed record
        borrowed = self.db.query_borrowed_book(book_id, "borrowed")
        if not borrowed:
            return False
        else:
            return True
    
    def borrow_book(self, book_id):
        today = datetime.datetime.now()
        due_date = today + timedelta(days=self.max_borrow_days)
        self.db.insert_borrowed_book(
            self.username,
            book_id,
            today,
            due_date,
        )
        

