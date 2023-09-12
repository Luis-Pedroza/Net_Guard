# ***************************************************
# FILE: UI_Ports_Tab.py
#
# DESCRIPTION: 
# TablePortsCreator is a class that facilitates the creation and setup of a Qt-based table for displaying data.
# It interacts with a database to retrieve relevant information and populates the table with that data.
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

from PyQt5 import QtCore, QtWidgets, QtGui
from Controller_Module.Ports import GetPortsData
from UI_Module.UI_Message import PopUpMessage


class TablePortsCreator(object):
    def __init__(self, port, protocol, service):
        self.data_table_ports = GetPortsData()
        self.error_message = PopUpMessage()
        self.port = port
        self.protocol = protocol.lower()
        self.service = service
        
    def setup_table(self, main_window):
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
            header = ['Port', 'Service', 'Protocol', 'Description', 'Reference' ]
            self.new_table.setColumnCount(5)
            self.new_table.setRowCount(rows)
            self.new_table.setHorizontalHeaderLabels(header)
            self.new_table.setGeometry(QtCore.QRect(1, 0, 759, 349))
            self.new_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.new_table.horizontalHeader().setSectionResizeMode(3,QtWidgets.QHeaderView.Stretch)
            self.new_table.cellDoubleClicked.connect(self.init_ports_window)

            for row_num, row_data in enumerate(ports_list):
                for col_num, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.new_table.setItem(row_num, col_num, item)
            
        else: self.new_table = QtWidgets.QTableWidget(main_window)

    def init_ports_window(self):
        code = 'This does not work'
        message = 'In development'
        icon = QtWidgets.QMessageBox.Information
        self.error_message.show_message(code, message, icon)