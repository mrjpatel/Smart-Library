class ConsoleMenu:
    """
    This Class is to handle the menu and getting user input.
    It is responsible for printing the menu and invoking the respective menu
    handler

    menu_handlers: list
        List of menu handlers to print and invoke
    message: str
        Message to print out before printing the menu
    """
    def __init__(self, menu_handlers, message):
        self.menu_handlers = menu_handlers
        self.message = message

    def display_menu(self):
        """
        Prints the menu out with an option for each menu handler
        """
        print("\n{}".format(self.message))
        for i, h in enumerate(self.menu_handlers):
            # iterate through handlers and display menu text
            print("\t{}. {}".format(i+1, h.get_display_text()))
        # add option for exiting the program
        print("\t{}. {}".format(0, "Exit"))

    def prompt_and_invoke_option(self):
        """
        Prompts the user to enter an option and invokes the respective
        menu handler that is selected
        """
        while True:
            print("\nSelect an option: ", end="")
            # get option from user, and strip whitespace
            str_option = input().strip()
            # validate input
            if (not str_option.isdigit()):
                # input not a number
                print("{} is not a valid option".format(str_option))
                continue
            # input is a number, check ranges
            option = int(str_option)
            if option == 0:
                # option 0 is exit
                return True
            elif option > len(self.menu_handlers):
                # option doesn't have a defined handler
                print("{} is not a valid option".format(option))
                continue

            # valid option, invoke handler
            self.menu_handlers[option-1].invoke()
            break
        # don't exit, display menu again
        return False