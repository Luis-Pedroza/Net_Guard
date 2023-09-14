# ***************************************************
# FILE: Ports.py
#
# DESCRIPTION:
# The GetPortsData class is designed to retrieve port
# information from a database. It connects to a SQLite database
# containing port data, performs queries, and handles exceptions
# using the PopUpMessage class.
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
from UserInterface.Alerts import PopUpMessage
from Database.Connection import DatabaseConnection


class GetPortsData():
    '''
    A class for retrieving port-related data from a database.

    Attributes:
        database (DatabaseConnection): Manages the connection to the database.
        popUpMessage (PopUpMessage): Handles exceptions and error messages.

    Methods:
        __init__(self)
            Initializes the GetPortsData class. It sets up the database connection and exception handling.

        get_all_ports(self, minimum: int, maximum: int) -> list
            Retrieves all port data for a given range of IDs between minimum and maximum values.

        get_search(self, port: int, protocol: str, service: str) -> list
            Retrieves port data based on search criteria, including port number, protocol, and service.

    '''
    def __init__(self):
        self.database = DatabaseConnection('Resources/ports.db')
        self.popUp_Message = PopUpMessage()

    def get_all_ports(self, minimum: int, maximum: int) -> list[tuple]:
        """
        Retrieves all port data for a given range of IDs between minimum and maximum values.

        Args:
            minimum (int): The minimum ID value.
            maximum (int): The maximum ID value.

        Returns:
            list: A list of rows from the Ports_Info table.

        Raises:
            Exception: If there is an issue with the database query.

        Example Usage:
            ports_data = GetPortsData()
            data = ports_data.get_all_ports(10, 24)

        """
        try:
            query = 'SELECT Port, Service, Protocol, Description, Reference  FROM Ports_Info WHERE ID >= ? AND ID <= ?'
            params = (minimum, maximum)
            self.database.connect()
            table = self.database.query(query, params)
            self.database.disconnect()
            return table
        except Exception as exception:
            self.popUp_Message.show_message('UNABLE_TO_USE_get_all_ports', exception, QMessageBox.Critical)
            return None

    def get_search(self, port: int, protocol: str, service: str) -> list[tuple]:
        """
        Retrieves port data based on search criteria, including port number, protocol, and service.

        Args:
            port (int): The port number to search for.
            protocol (str): The protocol to filter by ('TCP', 'UDP', or 'ambos').
            service (str): The service name to search for.

        Returns:
            list: A list of rows from the Ports_Info table that match the search criteria.

        Raises:
            Exception: If there is an issue with the database query.

        Example Usage:
            ports_data = GetPortsData()
            data = ports_data.get_search(80, 'TCP', 'http')
        """
        # if port is 0 then search by service and show both protocols (TCP & UDP)
        if protocol == 0 and port == 0:
            try:
                query = 'SELECT * FROM Ports_Info WHERE Service LIKE ?'
                params = ('%'+service+'%',)
                self.database.connect()
                table = self.database.query(query, params)
                self.database.disconnect()
                return table
            except Exception as exception:
                self.popUp_Message.show_message('UNABLE_TO_SEARCH_Both_Service', exception, QMessageBox.Critical)
                return None
        # if port isn't 0 then search by port and show both protocols (TCP & UDP)
        elif protocol == 0 and port != 0:
            try:
                query = 'SELECT * FROM Ports_Info WHERE Port == ?'
                params = (port,)
                self.database.connect()
                table = self.database.query(query, params)
                self.database.disconnect()
                return table
            except Exception as exception:
                self.popUp_Message.show_message('UNABLE_TO_SEARCH_Both_Ports', exception, QMessageBox.Critical)
                return None
        # if protocol isn't both specify the protocol
        else:
            if protocol == 1:
                str_protocol = 'tcp'
            else:
                str_protocol = 'udp'
            # if port is 0  then search by service and specify the protocol
            if port == 0:
                try:
                    query = 'SELECT * FROM Ports_Info WHERE Service LIKE ? AND Protocol == ?'
                    params = ('%'+service+'%', str_protocol)
                    self.database.connect()
                    table = self.database.query(query, params)
                    self.database.disconnect()
                    return table
                except Exception as exception:
                    self.popUp_Message.show_message('UNABLE_TO_SEARCH_Service', exception, QMessageBox.Critical)
                    return None
            # if port isn't 0 then search by port and specify the protocol
            else:
                try:
                    query = 'SELECT * FROM Ports_Info WHERE Port == ? AND Protocol == ?'
                    params = (port, str_protocol)
                    self.database.connect()
                    table = self.database.query(query, params)
                    self.database.disconnect()
                    return table
                except Exception as exception:
                    self.popUp_Message.show_message('UNABLE_TO_SEARCH_Both_Port', exception, QMessageBox.Critical)
                    return None


class TableCounter():
    '''
    A simple class to manage a counter that increments and decrements by 14 within a specified range.

    Attributes:
        - current_value (int): The current value of the counter.
        - min_value (int): The minimum value that the counter can reach.
        - max_value (int): The maximum value that the counter can reach.

    Methods:
        - __init__(self, min_value: int, max_value: int)
            Initializes the TableCounter with a minimum and maximum value.

        - next(self)
            Increments the counter by 14 if it's within the maximum range.

        - previous(self):
            Decrements the counter by 14 if it's above the minimum range.

    '''
    def __init__(self, min_value, max_value):
        '''
        Initializes the TableCounter with a minimum and maximum value.

        Args:
            min_value (int): The minimum value for the counter.
            max_value (int): The maximum value for the counter.

        Returns:
            None

        Example Usage:
            counter = TableCounter(0, 100)

        '''
        self.current_value = min_value
        self.min_value = min_value
        self.max_value = max_value

    def next(self):
        '''
        Increments the counter by 14 if it's within the maximum range.

        Args:
            None

        Returns:
            None

        Example Usage:
            counter = TableCounter(0, 100)
            counter.next()
            print(counter.current_value)  # Output: 14

        '''
        if self.current_value < self.max_value:
            self.current_value += 14

    def previous(self):
        '''
        Decrements the counter by 14 if it's above the minimum range.

        Args:
            None

        Returns:
            None

        Example Usage:
            counter = TableCounter(0, 100)
            counter.previous()
            print(counter.current_value)  # Output: 0

        '''
        if self.current_value > self.min_value:
            self.current_value -= 14
