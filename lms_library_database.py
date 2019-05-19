import mysql.connector
from mysql.connector import Error
import json


class LMSLibraryDatabase:
    book_schema = ["BookID","Title","Author","PublishDate"]
    user_schema = ["username", "first_name", "last_name", "email"]

    def __init__(self, db_settings_file):
        with open(db_settings_file) as json_file:  
            data = json.load(json_file)
            self.__host = data["host"]
            self.__database = data["database"]
            self.__user = data["user"]
            self.__password = data["password"]
        self.test_connection()

    def test_connection(self):
        try:
            # Open connection
            connection = mysql.connector.connect(
                host=self.__host,
                database=self.__database,
                user=self.__user,
                password=self.__password
            )
            # Check Connection
            if connection.is_connected() is False:
                raise Exception("Cannot connect to DB")
            # Close database connection
            if(connection.is_connected()):
                connection.close()
        except Error as e :
            print ("Error while connecting to MySQL", e)

    def query_book_by_id(self, book_id):
        # prepare statement
        query = """SELECT * FROM Book
                    WHERE BookID = %(book_id)s;"""
        # sanitize inputs    
        params = {
            "book_id": book_id
        }
        # executre query
        return self.__run_query(query, params)
    
    def query_book_by_author(self, author):
        # prepare statement
        query = """SELECT * FROM Book
                    WHERE Author = %(author)s;"""
        # sanitize inputs    
        params = {
            "author": author
        }
        # executre query
        return self.__run_query(query, params)
    
    def query_book_by_title(self, title):
        # prepare statement
        query = """SELECT * FROM Book
                    WHERE Title = %(title)s;"""
        # sanitize inputs    
        params = {
            "title": title
        }
        # executre query
        return self.__run_query(query, params)

    def query_book_by_publish_date(self, publish_date):
        # prepare statement
        query = """SELECT * FROM Book
                    WHERE PublishedDate = %(publish_date)s;"""
        # sanitize inputs    
        params = {
            "publish_date": publish_date
        }
        # executre query
        return self.__run_query(query, params)
    
    def get_user(self, username):
        # prepare statement
        query = """SELECT * FROM LmsUser
                    WHERE username = %(username)s;"""
        # sanitize inputs    
        params = {
            "username": username
        }
        # executre query
        return self.__run_query(query, params)
    
    def add_user(self, user):
        # prepare statement
        query = """INSERT INTO LmsUser (
                        username,
                        first_name,
                        last_name,
                        email
                    ) VALUES (
                        %(username)s,
                        %(first_name)s,
                        %(last_name)s,
                        %(email)s
                    );"""
        # sanitize inputs    
        params = {
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"]
        }
        # executre query
        self.__run_update(query, params)

    def update_user(self, user):
        # prepare statement
        query = """UPDATE LmsUser SET
                        first_name = %(first_name)s,
                        last_name = %(last_name)s,
                        email = %(email)s
                    WHERE username = %(username)s;"""
        # sanitize inputs    
        params = {
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"]
        }
        # executre query
        self.__run_update(query, params)

    def query_borrowed_book(self, book_id, status):
        # prepare statement
        query = """SELECT * FROM BookBorrowed
                    WHERE BookID = %(book_id)s
                    AND Status = %(status)s
                    ;"""
        # sanitize inputs    
        params = {
            "book_id": book_id,
            "status": status
        }
        # executre query
        return self.__run_query(query, params)
    
    def insert_borrowed_book(self, username, book_id, borrow_date, due_date):
        # prepare statement
        query = """INSERT INTO BookBorrowed (
                        LmsUsername,
                        BookID,
                        Status,
                        BorrowedDate,
                        DueDate
                    ) VALUES (
                        %(username)s,
                        %(book_id)s,
                        %(status)s,
                        %(borrow_date)s,
                        %(due_date)s
                    );"""
        # sanitize inputs    
        params = {
            "username": username,
            "book_id": book_id,
            "status": "borrowed",
            "borrow_date": borrow_date,
            "due_date": due_date,
        }
        # executre query
        self.__run_update(query, params)

    def __run_query(self, query, params):
        result = ""
        try:
            # Open connection
            connection = mysql.connector.connect(
                host=self.__host,
                database=self.__database,
                user=self.__user,
                password=self.__password
            )
            # Run Query
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query, params)
                result = cursor.fetchall()
        except Error as e :
            print ("Error while connecting to MySQL", e)
        finally:
            # Close database connection.
            if(connection.is_connected()):
                cursor.close()
                connection.close()
                return(result)
    
    def __run_update(self, query, params):
        result = ""
        try:
            # Open connection
            connection = mysql.connector.connect(
                host=self.__host,
                database=self.__database,
                user=self.__user,
                password=self.__password
            )
            # Run Query and commit
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query, params)
                connection.commit()
        except Error as e :
            print ("Error while connecting to MySQL", e)
        finally:
            # Close database connection.
            if(connection.is_connected()):
                cursor.close()
                connection.close()
                return(result)
