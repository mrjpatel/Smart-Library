from datetime import datetime
from datetime import timedelta

from lms_library_database import LMSLibraryDatabase
from menu_handler import MenuHandler
from google_calander import GoogleCalanderAPI


class ConsoleBorrowBook(MenuHandler):
    max_borrow_days = 7

    def __init__(self, database, user):
        self.db = LMSLibraryDatabase(database)
        self.display_text = "Borrow Book(s)"
        self.user = user

    def invoke(self):
        exit = False
        while not exit:
            self.start()
            print("Borrow another book? (y/n): ", end="")
            str_input = input().strip()
            if str_input is not "y":
                exit = True

    def start(self):
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
        book_item = self.db.query_book_by_id(book_id)
        if not book_item:
            print("Book with ID {} does not exist!".format(book_id))
            return
        book = dict()
        # convert to book dict
        for key, value in zip(LMSLibraryDatabase.book_schema, book_item[0]):
            book[key] = value
        # check if book is borrowed
        if self.is_borrowed(book):
            print("Book with ID {} is currently borrowed!".format(book_id))
            return
        self.borrow_book(book)

    def is_borrowed(self, book):
        # makes call to db to get borrowed record
        borrowed = self.db.query_borrowed_book(book["BookID"], "borrowed")
        if not borrowed:
            return False
        else:
            return True

    def borrow_book(self, book):
        # set date borrowed and due date
        today = datetime.now()
        due_date = today + timedelta(days=self.max_borrow_days)
        # generate event through google calander api
        event_id = GoogleCalanderAPI.create_due_event(
            due_date, book,
            self.user
        )
        # insert db record for borrowed book
        self.db.insert_borrowed_book(
            self.user["username"],
            book["BookID"],
            today,
            due_date,
            event_id
        )
        print(
            "Successfully borrowed book: " +
            "{}, Reminder to return sent!".format(book["Title"])
        )
