import sqlite3

class LMSUserDatabase:
    def __init__(self, db):
        self.db = db
        self.create_table()
    
    def create_table(self):       
        # read file containing the lms_user table schema
        with open("lms_user.sql", "r") as f:
            schema = f.read()
        # run on database to create table
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            c.execute(schema)
    
    def insert_user(self, credentials, first_name, last_name, email):
        # prepare insert
        insert = """INSERT INTO lms_user (
                        username,
                        encrypted_password,
                        first_name,
                        last_name,
                        email
                    ) VALUES (
                        :username,
                        :encrypted_password,
                        :first_name,
                        :last_name,
                        :email
                    );"""
        # sanitize inputs
        data = {
            "username": credentials.username,
            "encrypted_password": credentials.get_encrypted_password(),
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }
        # insert data into database
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            c.execute(insert, data)
    
    def get_user(self, credentials):
        # prepare statement
        select = """SELECT * FROM lms_user
                    WHERE username = :username;"""
        # sanitize inputs    
        data = {
            "username": credentials.username,
        }
        # get matching row
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            result_set = c.execute(select, data).fetchone()
            if result_set is None:
                # username not found
                return None

            # convert to dictionary for easy iteration
            columns = [
                "user_id",
                "username",
                "encrypted_password",
                "first_name",
                "last_name",
                "email"
            ]
            user = {}
            for i, c in enumerate(columns):
                user[c] = result_set[i]
                
        # validate password
        encrypted_password = user["encrypted_password"]
        is_valid = credentials.is_compare_cyphertext(encrypted_password)
        return user if is_valid else None

    def is_username_exists(self, username):
        # prepare statement
        select = """SELECT * FROM lms_user
                    WHERE username = :username;"""
        # sanitize inputs
        data = {
            "username": username
        }
        # check if username returns any records
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            return c.execute(select, data).fetchone() is not None
