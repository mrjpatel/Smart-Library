import mysql.connector
from mysql.connector import Error
import json


class LMSLibraryDatabase:
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

    def query_book_by_author(self, author):
        # prepare statement
        query = """SELECT * FROM Book
                    WHERE username = %(author)s;"""
        # sanitize inputs    
        params = {
            "author": author
        }
        # executre query
        return self.__run_query(query, params)

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
                cursor.execute(query)
                result = cursor.fetchall()
        except Error as e :
            print ("Error while connecting to MySQL", e)
        finally:
            # Close database connection.
            if(connection.is_connected()):
                cursor.close()
                connection.close()
                return(result)
