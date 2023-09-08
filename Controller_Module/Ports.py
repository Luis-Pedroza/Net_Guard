# ***************************************************
# FILE: Ports.py
#
# DESCRIPTION: 
# This code makes queries to the DB
# It either gets:
# 1. the 14 rows between the maximum and minimum values given
# 2. the values given for a search
# It also has a counter by 14 in 14
#
# AUTHOR: Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

from PyQt5.QtWidgets import QMessageBox
from DB_Module.Connection import DatabaseConnection
from UI_Module.UI_Message  import PopUpMessage

class Get_Data():
    # initialize the class
    def __init__(self):
        # name and location of the DB
        self.db = DatabaseConnection('Resources/ports.db')
        # use of PopUpMessage for exceptions
        self.popUpMessage = PopUpMessage()

    # Function to get the 14 rows between the maximum and minimum values given
    def get_all_ports(self, minimum, maximum):
        try:
            #query and parameters
            query = 'SELECT Port, Service, Protocol, Description, Reference  FROM Ports_Info WHERE ID >= ? AND ID <= ?'
            params = (minimum, maximum)
            #make connection, apply query and close connection.
            self.db.connect()
            table = self.db.query(query, params)    
            self.db.disconnect()
            return table
        except Exception as exception:
            self.popUpMessage.show_message('UNABLE_TO_USE_get_all_ports', exception, QMessageBox.Critical)
            return None

    # Function to get the values given for a search
    def get_search(self, port, protocol, service):
        #agregar opción para que busque conjuntos 3-4
        # if port is 0 then search by service and show both protocols (TCP & UDP)
        if protocol == 'ambos' and port == 0:
            try:
                query = 'SELECT * FROM Ports_Info WHERE Service LIKE ?'
                params = ('%'+service+'%',)
                self.db.connect()
                table = self.db.query(query, params) 
                self.db.disconnect()
                return table
            except Exception as exception:
                self.popUpMessage.show_message('UNABLE_TO_SEARCH_Both_Service', exception, QMessageBox.Critical)
                return None
        #if port is´nt 0 then search by port and show both protocols (TCP & UDP)         
        elif protocol == 'ambos' and port != 0:
            try:
                query = 'SELECT * FROM Ports_Info WHERE Port == ?'
                params = (port,)
                self.db.connect()
                table = self.db.query(query, params) 
                self.db.disconnect()
                return table
            except Exception as exception:
                self.popUpMessage.show_message('UNABLE_TO_SEARCH_Both_Ports', exception, QMessageBox.Critical)
                return None
            
        # if protocol is´nt ambos specify the protocol
        else:
            # if port is 0  then search by service and specify the protocol
            if port == 0:
                try:
                    query = 'SELECT * FROM Ports_Info WHERE Service LIKE ? AND Protocol == ?'
                    params = ('%'+service+'%', protocol)
                    self.db.connect()
                    table = self.db.query(query, params) 
                    self.db.disconnect()
                    return table
                except Exception as exception:
                    self.popUpMessage.show_message('UNABLE_TO_SEARCH_Service', exception, QMessageBox.Critical)
                    return None
            #if port is´nt 0 then search by port and specify the protocol
            else:
                try:
                    query = 'SELECT * FROM Ports_Info WHERE Port == ? AND Protocol == ?'
                    params = (port, protocol)
                    self.db.connect()
                    table = self.db.query(query, params) 
                    self.db.disconnect()
                    return table
                except Exception as exception:
                    self.popUpMessage.show_message('UNABLE_TO_SEARCH_Both_Port', exception, QMessageBox.Critical)
                    return None
                
# Counter of 14 by 14                
class Table_Counter():
    # initialize default values
    def __init__(self, min_value, max_value):
        self.current_value = min_value
        self.min_value = min_value
        self.max_value = max_value
                
    # count value plus 14                
    def next(self):
        if self.current_value < self.max_value:   
            self.current_value += 14
    # count value minus 14
    def previous(self):
        if self.current_value > self.min_value: 
            self.current_value -= 14

        
        
        
        
