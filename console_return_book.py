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

    def start(self):
        print("\nEnter BookID to return: ", end="")
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
        book_item = self.db.query_book_by_id(book_id)[0]
        if not book_item:
            print("Book with ID {} does not exist!".format(book_id))
            return
        book = dict()
        # convert to book dict
        for key, value in zip(LMSLibraryDatabase.book_schema, book_item):
            book[key] = value

        # check if book is borrowed
        borrowed_record = self.is_borrowed(book, self.user["username"])
        if not borrowed_record:
            print("Book with ID {} is not borrowed by you!".format(book_id))
            return
        self.return_book(borrowed_record)

    def is_borrowed(self, book_borrowed, username):
        """
        Function to check if a book is borrowed or not

        :param book: Book details of book to check
        :type book: dict
        :param username: Username of who would like to return book
        :type username: str
        :return: If book is borrowed
        :rtype: bool
        """
        # makes call to db to get borrowed record
        borrowed = self.db.query_borrowed_book_by_user(
            book_borrowed["BookID"],
            "borrowed",
            username
        )
        if not borrowed:
            return False
        else:
            print(borrowed)
            book = dict()
            # create dict from record
            for key, value in zip(
                LMSLibraryDatabase.book_borrow_schema,
                borrowed[0]
            ):
                book[key] = value
            print(book)
            return book

    def return_book(self, book_borrowed):
        """
        Function to return book
        
        :param book: Book details of book to check
        :type book: dict
        :return: No return
        """
        # set date return
        today = datetime.now()
        # generate event through google calander api
        GoogleCalanderAPI.delete_due_event(
            book_borrowed["EventID"]
        )
        # insert db record for borrowed book
        self.db.update_borrowed_book(
            book_borrowed["BookBorrowedID"],
            today
        )
        print(
            "Successfully Returned book: " +
            "{}, Reminder Deleted!".format(book_borrowed["BookID"])
        )
