from abc import ABC, abstractmethod

from lms_user_database import LMSUserDatabase

class MenuHandler(ABC):
    """
    Abstract class that is used for all the menu options

    db : LMSUserDatabase
        Database object
    display_text : str
        Display test for the console menu
    """
    def __init__(self, user_database):
        self.db = LMSUserDatabase(user_database)
        self.display_text = "Unknown menu option"

    def get_display_text(self):
        """
        function to get the display text of the menu handler
        """
        return self.display_text
    
    @abstractmethod
    def invoke(self):
        """
        Abstract function to invoke the child classes functionallity
        """
        pass
