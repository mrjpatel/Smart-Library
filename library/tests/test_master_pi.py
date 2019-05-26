import unittest
from unittest.mock import patch

from library.master.master_pi import MasterPi
from library.common.lms_library_database import LMSLibraryDatabase


class Test_Master_Pi(unittest.TestCase):
    def test_validate_user_dict_1(self):
        user = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@gmail.com",
            "username": "jsmith"
        }
        self.assertTrue(MasterPi.validate_user_dict(user))

    def test_validate_user_dict_2(self):
        user = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@gmail.com"
        }
        self.assertFalse(MasterPi.validate_user_dict(user))

    def test_validate_user_dict_3(self):
        user = {
            "first_name": "John",
            "last_name": "Smith",
            "username": "jsmith"
        }
        self.assertFalse(MasterPi.validate_user_dict(user))

    def test_validate_user_dict_4(self):
        user = {
            "first_name": "John",
            "email": "john.smith@gmail.com",
            "username": "jsmith"
        }
        self.assertFalse(MasterPi.validate_user_dict(user))

    def test_validate_user_dict_5(self):
        user = {
            "last_name": "Smith",
            "email": "john.smith@gmail.com",
            "username": "jsmith"
        }
        self.assertFalse(MasterPi.validate_user_dict(user))

    def test_validate_user_dict_6(self):
        user = {}
        self.assertFalse(MasterPi.validate_user_dict(user))

    def test_update_or_add_user_1(self):
        # Test user add
        user = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@gmail.com",
            "username": "jsmith"
        }
        test_db = "lms_library_config_test.json"
        db = LMSLibraryDatabase(test_db)
        user_list = list()
        user_list.append(user["username"])
        user_list.append(user["first_name"])
        user_list.append(user["last_name"])
        user_list.append(user["email"])
        MasterPi.update_or_add_user(test_db, user)
        db_user = db.get_user(user["username"])
        self.assertTupleEqual(tuple(user_list), db_user[0])

if __name__ == "__main__":
    unittest.main()
