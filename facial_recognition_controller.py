from menu_handler import MenuHandler
from face_login import FaceLogin


class FacialRecognitionController(MenuHandler):
    """
    Class for handling the face log in.
    It is used to start video stream to recognise face
    and attempting to authenitcate the user into the system

    user_database: str
        File path to the sqlite3 database
    """
    def __init__(self, user_database):
        """
        :param user_database: database for storing users on reception pi
        :type user_database: str
        """
        super().__init__(user_database)
        self.display_text = "Log in with face"

    def invoke(self):
        """
        Method that is called when the user selects the "Log in with face"
        option
        """
        print("Log in to the LMS\n")
        face = FaceLogin()
        user = face.recognise().strip()

        if user == "":
            print("Face not found")
            return

        self.connect_to_master_pi(user)

    def connect_to_master_pi(self, user):
        """
        Establishes a socket connection to the master pi
        :param user: The authenticated user
        :type user: dict
        """
        with open("socket.json", "r") as f:
            config = json.load(f)
            ip = config["master_pi_ip"]
            port = config["port"]
            dest = (ip, port)

        # Connect to master pi
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to Master Pi on {}:{}...".format(*dest))
            s.connect(dest)
            serial_user = pickle.dumps(user)
            s.send(serial_user)
            print("Logging in as user {}".format(user["username"]))
            while True:
                message = s.recv(1024).decode("utf-8").strip()
                if message == "exit":
                    logout_message = s.recv(1024).decode("utf-8")
                    break
                if message == "barcode":
                    data = QrScanner.get_qr_codes()
                    print(data)
                    s.send(pickle.dumps(data))
                    print("Please continue on Master Pi")
                if message == "voice":
                    # TODO: Voice Searching
                    pass
            print(logout_message)
