#!/usr/bin/env python3

import socket

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bind to port
        addr = ("", 32674)
        s.bind(addr)
        s.listen()
        print("Listening on {}:{}...".format(*addr))

        # listen for connections
        while True:
            client_conn, client_addr = s.accept()
            with client_conn as cc:
                print("Reception Pi connected at {}:{}".format(*client_addr))

if __name__ == "__main__":
    main()
