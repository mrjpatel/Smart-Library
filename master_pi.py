#!/usr/bin/env python3

import socket
import pickle
import json

from console_menu import ConsoleMenu
from console_search_book import ConsoleSearchBook

def main():
    # Load DB details from json
    db_details_file = "lms_library_config.json"

    # define menu handlers
    menu_handlers = [
        ConsoleSearchBook(db_details_file)
    ]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bind to port
        addr = ("", 32674)
        s.bind(addr)
        s.listen()
        print("Listening on {}:{}...".format(*addr))

        try:
            # listen for connections
            while True:
                print("Waiting for Reception Pi...")
                client_conn, client_addr = s.accept()
                with client_conn as cc:
                    print("Reception Pi connected at {}:{}".format(*client_addr))
                    # recieve user data
                    serial_data = cc.recv(1024)
                    user = pickle.loads(serial_data)

                    # display menu, get selection, and run
                    is_exit = False
                    while not is_exit:
                        menu = ConsoleMenu(
                            menu_handlers,
                            "Master Pi Menu: Welcome {}!".format(user["first_name"])
                        )
                        menu.display_menu()
                        is_exit = menu.prompt_and_invoke_option()
                    print("Goodbye!")

                    cc.sendall(b"Successfully Logged Out")
        finally:
            s.close()
                

if __name__ == "__main__":
    main()
