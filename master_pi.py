#!/usr/bin/env python3

import socket
import pickle
import json

from console_menu import ConsoleMenu
from console_search_book import ConsoleSearchBook
from lms_library_database import LMSLibraryDatabase 

class MasterPi:
    @staticmethod
    def start_master_pi():
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

                        cc.sendall(b"Successfully Logged Out")
            except KeyboardInterrupt:
                print("Keyboard Interrupt detected, shutting down...")
            finally:
                s.shutdown(socket.SHUT_RDWR)
                s.close()
    
    @staticmethod
    def update_or_add_user(db_location, user):
        db = LMSLibraryDatabase(db_location)
        db_user = db.get_user(user["username"])
        if not db_user:
            db.add_user(user)
        else:
            user["user_id"] = db_user[0]["user_id"]
            db.update_user(user)

    @staticmethod
    def validate_user_dict(user):
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
