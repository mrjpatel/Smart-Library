import mysql.connector
from mysql.connector import Error
import json


class LMSLibraryDatabase:
    """
    A class used to access the GCP MySql Database

    book_schema : list
        Database Schema for the Book Table
    user_schema : list
        Database Schema for the User Table
    book_borrow_schema : list
        Database Schema for the Book Borrow Table
    """
    book_schema = [
        "BookID",
        "Title",
        "Author",
        "PublishDate"
    ]
    user_schema = [
        "username",
        "first_name",
        "last_name",
        "email"
    ]
    book_borrow_schema = [
        "BookBorrowedID",
        "LmsUsername",
        "BookID",
        "Status",
        "BorrowedDate",
        "DueDate",
        "ReturnedDate",
        "EventID"
    ]

    def __init__(self, db_settings_file):
        """
        Creating an object of this class. Tests the Database connection

        :param db_settings_file: Database Setting File
        :type db_settings_file: string
        """
        with open(db_settings_file) as json_file:
            data = json.load(json_file)
            self.__host = data["host"]
            self.__database = data["database"]
            self.__user = data["user"]
            self.__password = data["password"]
        self.test_connection()

    def test_connection(self):
        """
        Tests the Database connection

        :raises: Database Connect Exception
        """
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

    def query_book_by_id(self, book_id):
        """
        Queries Database for books that match the given Book ID

        :param book_id: Book ID of the book
        :type book_id: str
        :return: returns book records with the same ID as book_id
        :rtype: list (dicts with book details)
        """
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
        """
        Queries Database for books that match the given Author

        :param author: Author of the book
        :type author: str
        :return: returns book records with the same Author as author
        :rtype: list (dicts with book details)
        """
        # prepare statement
        query = """SELECT * FROM Book
                    WHERE LOWER(Author) = LOWER(%(author)s);"""
        # sanitize inputs
        params = {
            "author": author
        }
        # executre query
        return self.__run_query(query, params)

    def query_book_by_title(self, title):
        """
        Queries Database for books that match the given Title

        :param title: Title of the book
        :type title: str
        :return: returns book records with the same Title as title
        :rtype: list (dicts with book details)
        """
        # prepare statement
        query = """SELECT * FROM Book
                    WHERE LOWER(Title) LIKE LOWER(%(title)s);"""
        # sanitize inputs
        params = {
            # contains match for LIKE clause
            "title": "%" + title + "%"
        }
        # executre query
        return self.__run_query(query, params)

    def query_book_by_publish_date(self, publish_date):
        """
        Queries Database for books that match the given Published Date

        :param publish_date: Published Date of the book
        :type publish_date: str
        :return: returns book records with the same Published Date as
        publish_date
        :rtype: list (dicts with book details)
        """
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
        """
        Inserts user into Database

        :param user: User Dict to enter into Database
        :type users: dict that conforms with user_schema
        :return: no return
        """
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
        """
        Updates user into Database

        :param user: User Dict to enter into Database
        :type user: dict that conforms with user_schema
        :return: no return
        """
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
        """
        Queries Database for borrowed boook

        :param book_id: Book ID of borrowed book
        :type book_id: str
        :param status: Status of borrowed book
        :type status: str
        :return: list of borrowed books with id and satus
        :rtype: list
        """
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

    def query_borrowed_book_by_user(self, book_id, status, username):
        """
        Queries Database for borrowed boook by a user

        :param book_id: Book ID of borrowed book
        :type book_id: str
        :param status: Status of borrowed book
        :type status: str
        :param username: Username of user who borrowed book
        :type username: str
        :return: list of borrowed books with id and satus
        :rtype: list
        """
        # prepare statement
        query = """SELECT * FROM BookBorrowed
                    WHERE BookID = %(book_id)s
                    AND Status = %(status)s
                    AND Lmsusername = %(username)s
                    ;"""
        # sanitize inputs
        params = {
            "book_id": book_id,
            "status": status,
            "username": username
        }
        # executre query
        return self.__run_query(query, params)

    def insert_borrowed_book(
        self,
        username,
        book_id,
        borrow_date,
        due_date,
        event_id
    ):
        """
        Addes borrowed book to the database

        :param username: Username of user who borrowed book
        :type username: str
        :param book_id: Book ID of borrowed book
        :type book_id: str
        :param borrow_date: Datetime of when the book is borrowed
        :type borrow_date: datetime
        :param due_date: Datetime of when the book is due
        :type due_date: datetime
        :param book_id: Event ID of calander event
        :type book_id: str
        :return: no return
        """
        # prepare statement
        query = """INSERT INTO BookBorrowed (
                        LmsUsername,
                        BookID,
                        Status,
                        BorrowedDate,
                        DueDate,
                        EventID
                    ) VALUES (
                        %(username)s,
                        %(book_id)s,
                        %(status)s,
                        %(borrow_date)s,
                        %(due_date)s,
                        %(event_id)s
                    );"""
        # sanitize inputs
        params = {
            "username": username,
            "book_id": book_id,
            "status": "borrowed",
            "borrow_date": borrow_date,
            "due_date": due_date,
            "event_id": event_id
        }
        # executre query
        self.__run_update(query, params)

    def update_borrowed_book(
        self,
        record_id,
        return_date
    ):
        """
        Updates borrowed book with return date

        :param record_id: Record ID of borrowed book record
        :type record_id: int
        :param due_date: Datetime of when the book is returned
        :type due_date: datetime
        :return: no return
        """
        # prepare statement
        query = """UPDATE BookBorrowed SET
                        Status = %(status)s,
                        ReturnedDate = %(return_date)s
                    WHERE BookBorrowedID = %(record_id)s
                    """
        # sanitize inputs
        params = {
            "status": "returned",
            "return_date": return_date,
            "record_id": record_id
        }
        # executre query
        self.__run_update(query, params)

    def __run_query(self, query, params):
        """
        Executes Query with the Database

        :param query: SQL Query to execute
        :type query: str
        :param params: Parameters for the SQL Query
        :type params: dict
        :return: Query Result
        :rtype: list
        """
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
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            # Close database connection.
            if(connection.is_connected()):
                cursor.close()
                connection.close()
                return(result)

    def __run_update(self, query, params):
        """
        Executes Database Insert or Update

        :param query: SQL Query to execute
        :type query: str
        :param params: Parameters for the SQL Query
        :type params: dict
        :return: Query Result
        :rtype: list
        """
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
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            # Close database connection.
            if(connection.is_connected()):
                cursor.close()
                connection.close()
                return(result)
