import os
import socket

class SocketConnection:
    def __init__(self):
        self.destination_ip = os.getenv("LMS_MASTER_PI_IP", "")
        self.destination_port = 32674
    
    def send_json(self, object):
        # TODO
        pass
    
    def receive_json(self):
        # TODO
        pass
