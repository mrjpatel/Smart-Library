#!/usr/bin/env python3

import sys

from console_login import ConsoleLogin
from reception_pi_menu import ReceptionPiMenu


def main(argv):
    # validate command line arguments
    if len(argv) != 2:
        print("Usage: python3 reception_pi.py database")
        return
    else:
        db_location = argv[1]

    # define menu handlers
    menu_handlers = [
        ConsoleLogin(db_location)
    ]
    # display menu, get selection, and run
    is_exit = False
    while not is_exit:
        menu = ReceptionPiMenu(menu_handlers)
        menu.display_menu()
        is_exit = menu.prompt_and_invoke_option()


if __name__ == "__main__":
    main(sys.argv)
