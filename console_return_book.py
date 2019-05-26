from datetime import datetime
from datetime import timedelta

from lms_library_database import LMSLibraryDatabase
from menu_handler import MenuHandler
from google_calander import GoogleCalanderAPI


class ConsoleReturnBook(MenuHandler):
    """
    A class to handle the customer returning a book

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
        Function that is called to invoke the return book function.
        Gets the user input and validates if it is in a vaild book id format
        """
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
        self.start(book_id)

    def start(self, book_id):
        """
        This fuction is responsible for returning a book.
        It takes the book id given by the user and checks if it is borrowed by
        the user and then returns the book, deleting the calander invite

        :param book_id: Book ID of the book to return
        :type book_id: int
        :return: No return
        """
        # check if book exists
        book_item = self.db.query_book_by_id(book_id)[0]
        if not book_item:
            print("Book with ID {} does not exist!".format(book_id))
            return
        book = dict()
        # convert to book dict
        for key, value in zip(LMSLibraryDatabase.book_schema, book_item):
            book[key] = value
        print("Returning {} by {}...".format(book["Title"], book["Author"]))
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
            book = dict()
            # create dict from record
            for key, value in zip(
                LMSLibraryDatabase.book_borrow_schema,
                borrowed[0]
            ):
                book[key] = value
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
