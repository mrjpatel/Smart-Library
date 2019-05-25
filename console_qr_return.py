from datetime import datetime
from datetime import timedelta
import socket
import pickle

from lms_library_database import LMSLibraryDatabase
from menu_handler import MenuHandler
from console_return_book import ConsoleReturnBook


class ConsoleQRReturnBook(MenuHandler):
    """
    A class to handle the customer returning a book using a QR code

    max_borrow_days : int
        Number of days to borrow a book
    db : LMSLibraryDatabase
        Database object of the master database
    display_text : str
        Display test for the console menu
    user : dict
        User Object following the LMSLibraryDatabase.user_schema
    cs : obj
        Reception Socket connection object
    """
    max_borrow_days = 7

    def __init__(self, database, user, cc):
        """
        :param database: Database Setting File location
        :type database: string
        :param user: User Object following the LMSLibraryDatabase.user_schema
        :type user: dict
        :param cc: Client Connection Object of the Reception Pi
        :type cc: obj
        """
        self.database = database
        self.db = LMSLibraryDatabase(database)
        self.display_text = "Return Book(s) using Barcode"
        self.user = user
        self.cc = cc

    def invoke(self):
        """
        Function that is called to invoke the return book function
        """
        self.start()

    def start(self):
        self.cc.sendall(b"barcode")
        print("Please scan QR Code via Reception Pi")
        data = pickle.loads(self.cc.recv(1024))
        print(data)
        return_book = ConsoleReturnBook(self.database, self.user)
        if not data:
            print("Invaild Barcode!")
            return
        for book in data:
            if not book["BookID"]:
                print("Invalid Barcode!")
                return
            return_book.start(book["BookID"])
