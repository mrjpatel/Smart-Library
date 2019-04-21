from abc import ABC, abstractmethod

class MenuHandler(ABC):
    def __init__(self, user_database):
        self.user_database = user_database
        self.display_text = "Unknown menu option"

    def get_display_text(self):
        return self.display_text
    
    @abstractmethod
    def invoke(self):
        pass
