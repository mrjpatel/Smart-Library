from menu_handler import MenuHandler

class ConsoleRegister(MenuHandler):
    def __init__(self, user_database):
        super().__init__(user_database)
        self.display_text = "Register"
    
    def invoke(self):
        # TODO
        print("REGISTER...")
