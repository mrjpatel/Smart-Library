from abc import ABC, abstractmethod

from lms_library_database import LMSLibraryDatabase

class MasterMenuHandler(ABC):
    def __init__(self, database_config):
        self.db = LMSLibraryDatabase(database_config)
        self.display_text = "Unknown menu option"

    def get_display_text(self):
        return self.display_text
    
    @abstractmethod
    def invoke(self):
        pass
