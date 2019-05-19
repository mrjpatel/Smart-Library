from datetime import datetime
from dateutil.parser import parse

from lms_library_database import LMSLibraryDatabase
from menu_handler import MenuHandler
from console_menu import ConsoleMenu
from prettytable import PrettyTable

class ConsoleSearchBook(MenuHandler):

    def __init__(self, database):
        self.db = LMSLibraryDatabase(database)
        self.display_text = "Search Book"

    def invoke(self):
        # set menu handlers
        menu_handlers = [
            SearchByAuthor(self.db),
            SearchByName(self.db),
            SearchByPublishedDate(self.db)
        ]

        # display menu, get selection, and run
        is_exit = False
        while not is_exit:
            menu = ConsoleMenu(
                menu_handlers,
                "Search Book:"
            )
            menu.display_menu()
            is_exit = menu.prompt_and_invoke_option()
    
    @staticmethod
    def display_books(results):
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
    

class SearchByAuthor(MenuHandler):
    def __init__(self, database):
        self.db = database
        self.display_text = "Search by Author"

    def invoke(self):
        print("\nEnter Author Name: ", end="")
        # get option from user, and strip whitespace
        str_option = input().strip()
        if not str_option:
            print("Invalid Input!")
            return
        ConsoleSearchBook.display_books(
            self.db.query_book_by_author(str_option)
        )


class SearchByName(MenuHandler):
    def __init__(self, database):
        self.db = database
        self.display_text = "Search by Book Title"

    def invoke(self):
        print("\nEnter Book Name: ", end="")
        # get option from user, and strip whitespace
        str_option = input().strip()
        if not str_option:
            print("Invalid Input!")
            return
        ConsoleSearchBook.display_books(
            self.db.query_book_by_title(str_option)
        )


class SearchByPublishedDate(MenuHandler):
    def __init__(self, database):
        self.db = database
        self.display_text = "Search by Published Date"

    def invoke(self):
        print("\nEnter Published Date (YYYY-MM-DD): ", end="")
        # get option from user, and strip whitespace
        str_option = input().strip()
        # try parse as datetime object
        try:
            publish_date = parse(str_option)
            ConsoleSearchBook.display_books(
                self.db.query_book_by_publish_date(publish_date)
            )
        except:
            print("Invalid Input!")
            return
