import subprocess

from prettytable import PrettyTable

from console_menu import ConsoleMenu
from lms_library_database import LMSLibraryDatabase
from menu_handler import MenuHandler
from voice_search import VoiceSearch


class VoiceSearchBook(MenuHandler):
    """
    Class to handle searching for a book through voice
    db: LMSLibraryDatabase
        Database object of the master database
    """

    def __init__(self, database):
        """
        Creates a handler object
        :param databse: Database setting file location
        :type database: str
        """
        self.db = LMSLibraryDatabase(database)
        self.display_text = "Search Book by voice"

    def invoke(self):
        """
        Method that is called to invoke search for a book by voice
        """
        # set menu handlers
        menu_handlers = [
            VoiceSearchByAuthor(self.db),
            VoiceSearchByName(self.db)
        ]

        # display menu, get selection, and run
        is_exit = False
        while not is_exit:
            menu = ConsoleMenu(
                menu_handlers,
                "Search Book by voice:"
            )
            menu.display_menu()
            is_exit = menu.prompt_and_invoke_option()

    @staticmethod
    def display_books(results):
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


class VoiceSearchByAuthor(MenuHandler):
    """
    Class to handle searching for voice searching a book by name
    db: LMSLibraryDatabase
        Database object of the master database
    display_text: str
        Display text for the menu
    """

    def __init__(self, database):
        """
        :param database: Database setting file location
        :type database: str
        """
        self.db = database
        self.display_text = "Voice search by Author"

    def invoke(self):
        """
        Search for books by author using voice
        """
        voice = VoiceSearch()
        # clear screen of errors
        subprocess.run("clear")
        print("\nPrepare to say Author Name")
        search_term = voice.speech_to_text()
        if search_term is None:
            print("Error: could not perform search")
            return
        VoiceSearchBook.display_books(
            self.db.query_book_by_author(search_term)
        )


class VoiceSearchByName(MenuHandler):
    """
    Class to handle searching for voice searching a book by name
    db: LMSLibraryDatabase
        Database object of the master database
    display_text: str
        Display text for the menu
    """

    def __init__(self, database):
        """
        :param database: Database setting file location
        :type database: str
        """
        self.db = database
        self.display_text = "Voice search by Book Title"

    def invoke(self):
        """
        Search for books by name using voice
        """
        voice = VoiceSearch()
        # clear screen of errors
        subprocess.run("clear")
        print("\nPrepare to say Book Title")
        search_term = voice.speech_to_text()
        if search_term is None:
            print("Error: could not perform search")
            return
        VoiceSearchBook.display_books(
            self.db.query_book_by_title(search_term)
        )
