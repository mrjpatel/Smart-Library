#!/usr/bin/env python3

import sys

from library.common.console_menu import ConsoleMenu
from .console_login import ConsoleLogin
from .console_register import ConsoleRegister
from .facial_recognition_controller import FacialRecognitionController


def main(argv):
    """
    The main entry point for the Reception Pi
    """
    # validate command line arguments
    if len(argv) != 2:
        print("Usage: python3 reception_pi.py database")
        return
    else:
        db_location = argv[1]

    # define menu handlers
    menu_handlers = [
        ConsoleRegister(db_location),
        ConsoleLogin(db_location),
        FacialRecognitionController(db_location)
    ]
    # display menu, get selection, and run
    is_exit = False
    while not is_exit:
        menu = ConsoleMenu(menu_handlers, "Welcome to the library!")
        menu.display_menu()
        is_exit = menu.prompt_and_invoke_option()


if __name__ == "__main__":
    main(sys.argv)
