#!/usr/bin/env python3

import socket
import pickle
import json

from console_menu import ConsoleMenu
from console_search_book import ConsoleSearchBook
from console_borrow_book import ConsoleBorrowBook
from console_return_book import ConsoleReturnBook
from console_qr_return import ConsoleQRReturnBook
from lms_library_database import LMSLibraryDatabase


class MasterPi:
    """
    A class used to Launch the Master Pi
    """
    @staticmethod
    def start_master_pi():
        """
        This method is called to start the master pi
        """
        # Load DB details from json
        db_details_file = "lms_library_config.json"

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
                        print("Reception Pi connected at {}:{}".format(
                            *client_addr)
                        )
                        # recieve user data
                        serial_data = cc.recv(1024)
                        user = pickle.loads(serial_data)

                        if(not MasterPi.validate_user_dict(user)):
                            print("Invalid User Dict recieved")
                            cc.sendall(b"Invalid User Details recieved")
                            continue
                        MasterPi.update_or_add_user(db_details_file, user)

                        # define menu handlers
                        menu_handlers = [
                            ConsoleSearchBook(db_details_file, user),
                            ConsoleBorrowBook(db_details_file, user),
                            ConsoleReturnBook(db_details_file, user),
                            ConsoleQRReturnBook(db_details_file, user, cc)
                        ]

                        # display menu, get selection, and run
                        is_exit = False
                        while not is_exit:
                            menu = ConsoleMenu(
                                menu_handlers,
                                "Master Pi Menu: Welcome {}!".format(
                                    user["first_name"]
                                )
                            )
                            menu.display_menu()
                            is_exit = menu.prompt_and_invoke_option()
                        print("Goodbye!")

                        cc.sendall(b"exit")
                        cc.sendall(b"Successfully Logged Out")
            except KeyboardInterrupt:
                print("Keyboard Interrupt detected, shutting down...")

    @staticmethod
    def update_or_add_user(db_location, user):
        """
        Updates or addes the user to the Master Database

        :param user: User Dict to enter into Database
        :type users: dict that passes validate_user_dict
        :return: Record from the database
        :rtype: dict that conforms with user_schema
        """
        db = LMSLibraryDatabase(db_location)
        db_user = db.get_user(user["username"])
        if not db_user:
            db.add_user(user)
        else:
            db.update_user(user)

    @staticmethod
    def validate_user_dict(user):
        """
        Validates the user details sent from the Reception Pi to the Master Pi

        :param user: User sent from Reception Pi
        :type users: dict
        :return: If user dict is vaild
        :rtype: blol
        """
        if (
            "first_name" not in user or
            "last_name" not in user or
            "email" not in user or
            "username" not in user
        ):
            return False
        else:
            return True


if __name__ == "__main__":
    MasterPi.start_master_pi()
