from library.common.menu_handler import MenuHandler
from .console_login import ConsoleLogin
from .face_login import FaceLogin


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
        self.database = user_database
        super().__init__(user_database)
        self.display_text = "Log in with face"

    def invoke(self):
        """
        Method that is called when the user selects the
        "Log in with face" option
        """
        print("Log in to the LMS\n")
        face = FaceLogin()
        user = face.recognise().strip()

        if user == "":
            print("Face not found")
            return

        user_dict = self.db.get_user(user)
        login = ConsoleLogin(self.database)
        login.connect_to_master_pi(user_dict)
