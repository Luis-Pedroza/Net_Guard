# ***************************************************
# FILE: Connection.py
#
# DESCRIPTION:
# This script defines a class, 'DatabaseConnection',
# which facilitates the interaction with an SQLite database.
# It provides methods to establish a connection, disconnect,
# and execute queries on the database.
#
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

import sqlite3
from PyQt5.QtWidgets import QMessageBox
from UserInterface.Alerts import PopUpMessage


class DatabaseConnection():
    """
    A class for interacting with a SQLite database.

    Attributes:
        popUpMessage (PopUpMessage): Class for handling exceptions.
        icon (QMessageBox.Icon): An icon for message boxes in case of errors.
        db_name (str): The name of the database.
        connection (sqlite3.Connection): The SQLite database connection.

    Methods:
        __init__(self, db_name: str)
            Initialize the Database class.

        connect(self)
            Establish a connection to the database.

        disconnect(self)
            Close the connection to the database.

        query(self, query: str, params=None)
            Execute a query on the database and retrieve data.

    """
    def __init__(self, db_name: str):
        self.popUp_Message = PopUpMessage()
        self.icon = QMessageBox.Critical
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the database.

        Args:
            None

        Returns:
            None

        Raises:
            sqlite3.Error if there is an issue while connecting to the database.

        Example Usage:
            db = DatabaseConnection('my_database.db')
            db.connect()

        """
        try:
            self.connection = sqlite3.connect(self.db_name)
        except sqlite3.Error as exception:
            self.popUp_Message.show_message('ERROR_CONNECT_DB', exception, self.icon)

    def disconnect(self):
        '''
        Closes the connection to the database.

        Args:
            None

        Returns:
            None

        Raises:
            sqlite3.Error if there is an issue while disconnecting from the database.

        Example Usage:
            db = DatabaseConnection('my_database.db')
            db.connect()
            db.disconnect()

        '''
        try:
            self.connection.close()
        except sqlite3.Error as exception:
            self.popUp_Message.show_message('ERROR_DISCONNECT_DB', exception, self.icon)

    def query(self, query: str, params: tuple = None) -> list[tuple]:
        """
        Executes a query on the database and retrieves data.

        Args:
            query (str): The SQL query to execute.
            params (tuple): Parameters for the query, if needed.

        Returns:
            list: The fetched data from the query.

        Raises:
            sqlite3.Error if there is an issue while executing the query.

        Example Usage:
            db = DatabaseConnection('my_database.db')
            db.connect()
            data = db.query('SELECT * FROM my_table')
            db.disconnect()

        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
        except sqlite3.Error as exception:
            self.popUp_Message.show_message('ERROR_QUERY_DB', exception, self.icon)
