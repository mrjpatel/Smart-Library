from menu_handler import MenuHandler
from face_login import FaceLogin


class FacialRecognitionController(MenuHandler):

    def __init__(self, user_database):
        """
        :param user_database: database for storing users on reception pi
        :type user_database: str
        """
        super().__init__(user_database)
        self.display_text = "Log in with face"

    def invoke(self):
        """
        Method that is called when the user selects the "Log in" option
        """
        print("Log in to the LMS\n")
        face = FaceLogin()
        user = face.recognise().strip()

        while user == "":
            print("Face not registered.")
            key = input("Press e to exit or ENTER to re-login using face: ")
            if key == "e":
                return
            if key == "\n":
                user = face.recognise().strip()

        self.connect_to_master_pi(user)

    def connect_to_master_pi(self, user):
        """
        Establishes a socket connection to the master pi
        :param user: The authenticated user
        :type user: dict
        """
        # TODO: remove hardcoded destination
        dest = ("localhost", 32674)

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
