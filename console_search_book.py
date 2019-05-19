from lms_library_database import LMSLibraryDatabase
from menu_handler import MenuHandler
from console_menu import ConsoleMenu

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
    def display_resulsts(results):
        pass
        

class SearchByAuthor(MenuHandler):
    def __init__(self, database):
        self.db = database
        self.display_text = "Search by Author"

    def invoke(self):
        print("\nEnter Author Name ", end="")
        # get option from user, and strip whitespace
        str_option = input().strip()
        if not str_option:
            print("Invalid Input!")
            return
        self.db.query_book_by_author(str_option)


class SearchByName(MenuHandler):
    def __init__(self, database):
        self.db = database
        self.display_text = "Search by Book Title"

    def invoke(self):
        pass


class SearchByPublishedDate(MenuHandler):
    def __init__(self, database):
        self.db = database
        self.display_text = "Search by Publish Date"

    def invoke(self):
        pass