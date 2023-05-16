# ***************************************************
# FILE: Connection.py
#
# DESCRIPTION: 
# This code connect, disconnect and makes a query to a DB
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

import sqlite3
from PyQt5.QtWidgets import QMessageBox
from UI_Module.UI_Error import PopUp_Messages

class Database:
    #initialize  the class
    def __init__(self, db_name):
        # use  the PopUp_Messages for exceptions
        self.popUpMessage = PopUp_Messages()
        self.icon = QMessageBox.Critical
        # gets the name of the DB and initialize a connection
        self.db_name = db_name
        self.connection = None
        
    # connection to the DB
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
        except sqlite3.Error as exception:
            self.popUpMessage.showMessage('ERROR_CONNECT_DB', exception, self.icon)

    # disconnect to DB
    def disconnect(self):
        try:
            self.connection.close()
        except sqlite3.Error as exception:
            self.popUpMessage.showMessage('ERROR_DISCONNECT_DB',exception, self.icon)
            
    #Query to the DB        
    def query(self, query, params = None):
        try:
            cursor = self.connection.cursor()
            #if the query needs parameters
            if params:
                cursor.execute(query, params)
            #if the query does´nt need parameters
            else:
                cursor.execute(query)   
            #either way it commits the query and returns the data
            self.connection.commit()
            return cursor.fetchall()
        except sqlite3.Error as exception:
            self.popUpMessage.showMessage('ERROR_QUERY_DB' ,exception, self.icon)
        



