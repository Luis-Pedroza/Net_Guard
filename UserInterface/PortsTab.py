# ***************************************************
# FILE: UI_Ports_Tab.py
#
# DESCRIPTION:
# The TablePortsCreator class is used to create and set up
# a table for displaying network ports information based on
# specified search criteria, including port number,
# protocol (TCP/UDP), and service name.
# It utilizes the GetPortsData class for querying port information
# and the PopUpMessage class for error messages.
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

from PyQt5 import QtCore, QtWidgets, QtGui
from Controller.Ports import GetPortsData
from UserInterface.Alerts import PopUpMessage


class TablePortsCreator(object):
    """
    A class for creating and setting up a table to display network ports information.

    Attributes:
        data_table_ports (GetPortsData): An object for querying port information.
        error_message (PopUpMessage): A class for displaying error messages.
        port (int): The port number to search for.
        protocol (str): The protocol (TCP/UDP) to filter the search.
        service (str): The service name to filter the search.

    Methods:
        __init__(self, port: int, protocol: str, service: str)
            Initialize the TablePortsCreator class with search parameters.

        setup_table(self, MainWindow: QtWidgets.QMainWindow)
            Set up the table to display port information based on search criteria.

        init_ports_window(self)
            Show a message indicating that the init_ports_window function is under construction.

    """
    def __init__(self, port: int, protocol: str, service: str):
        """
        Initializes the TablePortsCreator class with search parameters.

        Args:
            port (int): The port number to search for.
            protocol (str): The protocol (TCP/UDP) to filter the search.
            service (str): The service name to filter the search.

        """
        self.data_table_ports = GetPortsData()
        self.error_message = PopUpMessage()
        self.port = port
        self.protocol = protocol.lower()
        self.service = service

    def setup_table(self, main_window: QtWidgets.QMainWindow):
        """
        Set up the table to display port information based on search criteria.

        Args:
            MainWindow (QtWidgets.QMainWindow): The main window to display the table.

        Returns:
            None

        Raises:
            None

        Example Usage:
            table_creator = TablePortsCreator(80, "tcp", "http")
            table_creator.setup_table(main_window)

        """
        main_window.setObjectName("main_window")
        main_window.setFixedSize(760, 350)
        main_window.setWindowTitle("Search")
        main_window.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        flags = main_window.windowFlags()
        main_window.setWindowFlags(flags & ~QtCore.Qt.WindowContextHelpButtonHint)

        ports_list = self.data_table_ports.get_search(self.port, self.protocol, self.service)

        if ports_list:
            rows = len(ports_list)
            self.new_table = QtWidgets.QTableWidget(main_window)
            header = ['Port', 'Service', 'Protocol', 'Description', 'Reference']
            self.new_table.setColumnCount(5)
            self.new_table.setRowCount(rows)
            self.new_table.setHorizontalHeaderLabels(header)
            self.new_table.setGeometry(QtCore.QRect(1, 0, 759, 349))
            self.new_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.new_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
            self.new_table.cellDoubleClicked.connect(self.init_ports_window)

            for row_num, row_data in enumerate(ports_list):
                for col_num, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.new_table.setItem(row_num, col_num, item)

        else: self.new_table = QtWidgets.QTableWidget(main_window)

    def init_ports_window(self):
        """
        init_ports_window should show specific information about the selected port
        Method under construction

        """
        code = 'This does not work'
        message = 'In development'
        icon = QtWidgets.QMessageBox.Information
        self.error_message.show_message(code, message, icon)
