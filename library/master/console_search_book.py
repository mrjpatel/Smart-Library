from datetime import datetime
from dateutil.parser import parse
from prettytable import PrettyTable

from library.common.lms_library_database import LMSLibraryDatabase
from library.common.menu_handler import MenuHandler
from library.common.console_menu import ConsoleMenu
from .console_borrow_book import ConsoleBorrowBook


class ConsoleSearchBook(MenuHandler):
    """
    A class to handle the customer searching a book

    db : LMSLibraryDatabase
        Database object of the master database
    display_text : str
        Display test for the console menu
    """
    def __init__(self, database, user):
        """
        :param database: Database Setting File location
        :type database: string
        """
        self.db = LMSLibraryDatabase(database)
        self.display_text = "Search Book by text"
        self.user = user
        self.database = database

    def invoke(self):
        """
        Function that is called to invoke the search book function
        """
        # set menu handlers
        menu_handlers = [
            SearchByAuthor(self.db, self),
            SearchByName(self.db, self),
            SearchByPublishedDate(self.db, self)
        ]

        # display menu, get selection, and run
        is_exit = False
        while not is_exit:
            menu = ConsoleMenu(
                menu_handlers,
                "Search Book by text:"
            )
            menu.display_menu()
            is_exit = menu.prompt_and_invoke_option()

    def display_books(self, results):
        """
        Function to display the books in a table

        :param results: Results of books to display
        :type results: list
        :return: No return
        """
        # Check if result is blank
        if not results:
            print("\nNo Books found!!")
            return
        # construct table and print
        book_schema = LMSLibraryDatabase.book_schema
        table = PrettyTable()
        table.field_names = book_schema
        for result in results:
            table.add_row(result)
        print("\n{}".format(table))
        self.prompt_borrow_book()

    def prompt_borrow_book(self):
        print("Would you like to borrow a book? (y/n): ", end="")
        str_input = input().strip()
        if str_input == "y":
            borrow_handler = ConsoleBorrowBook(self.database, self.user)
            borrow_handler.invoke()


class SearchByAuthor(MenuHandler):
    """
    A class to handle the customer searching by Author

    db : LMSLibraryDatabase
        Database object of the master database
    display_text : str
        Display test for the console menu
    """
    def __init__(self, database, sbh):
        """
        :param database: Database Setting File location
        :type database: string
        :param sbh: SearchBook Handler Object
        :type database: obj
        """
        self.db = database
        self.sbh = sbh
        self.display_text = "Search by Author"

    def invoke(self):
        """
        Function to search books by Author

        :return: No return
        """
        print("\nEnter Author Name: ", end="")
        # get option from user, and strip whitespace
        str_option = input().strip()
        if not str_option:
            print("Invalid Input!")
            return
        self.sbh.display_books(
            self.db.query_book_by_author(str_option)
        )


class SearchByName(MenuHandler):
    """
    A class to handle the customer searching by Name

    db : LMSLibraryDatabase
        Database object of the master database
    display_text : str
        Display test for the console menu
    """
    def __init__(self, database, sbh):
        """
        :param database: Database Setting File location
        :type database: string
        :param sbh: SearchBook Handler Object
        :type database: obj
        """
        self.db = database
        self.sbh = sbh
        self.display_text = "Search by Book Title"

    def invoke(self):
        """
        Function to search books by Name

        :return: No return
        """
        print("\nEnter Book Name: ", end="")
        # get option from user, and strip whitespace
        str_option = input().strip()
        if not str_option:
            print("Invalid Input!")
            return
        self.sbh.display_books(
            self.db.query_book_by_title(str_option)
        )


class SearchByPublishedDate(MenuHandler):
    """
    A class to handle the customer searching by Published Date

    db : LMSLibraryDatabase
        Database object of the master database
    display_text : str
        Display test for the console menu
    """
    def __init__(self, database, sbh):
        """
        :param database: Database Setting File location
        :type database: string
        :param sbh: SearchBook Handler Object
        :type database: obj
        """
        self.db = database
        self.sbh = sbh
        self.display_text = "Search by Published Date"

    def invoke(self):
        """
        Function to search books by Published Date

        :return: No return
        """
        print("\nEnter Published Date (YYYY-MM-DD): ", end="")
        # get option from user, and strip whitespace
        str_option = input().strip()
        # try parse as datetime object
        try:
            publish_date = parse(str_option)
            self.sbh.display_books(
                self.db.query_book_by_publish_date(publish_date)
            )
        except:
            print("Invalid Input!")
            return
