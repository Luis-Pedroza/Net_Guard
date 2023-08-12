# ***************************************************
# FILE: UI_Ports_Tab.py
#
# DESCRIPTION: 
# Table_Creator is a class that facilitates the creation and setup of a Qt-based table for displaying data.
# It interacts with a database to retrieve relevant information and populates the table with that data.
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

from PyQt5 import QtCore, QtWidgets, QtGui
from Controller_Module.Ports import Get_Data
from UI_Module.UI_Error import PopUp_Messages


class Table_Creator(object):
    #Initialize the class
    def __init__(self, port, protocol, service):
        # create a new object Get_Data to make an sql query
        self.data_table_ports = Get_Data()
        self.errorMessage = PopUp_Messages()
        # get the data to search for
        self.port = port
        self.protocol = protocol.lower()
        self.service = service
        
    # setup of the table    
    def setupTable(self, MainWindow):
        #initialize the main window with the specifications
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(760, 350)
        MainWindow.setWindowTitle("Búsqueda")
        MainWindow.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        flags = MainWindow.windowFlags()
        MainWindow.setWindowFlags(flags & ~QtCore.Qt.WindowContextHelpButtonHint)

        # get the data from the DB through the function get_search
        dataList = self.data_table_ports.get_search(self.port, self.protocol, self.service)

        # if there´s data
        if dataList:
            # get number of rows
            rows = len(dataList)
            # initialize widget with the specifications 
            self.newTable = QtWidgets.QTableWidget(MainWindow)
            header = ['Puerto', 'Servicio', 'Protocolo', 'Descripción', 'Referencia' ]
            self.newTable.setColumnCount(5)
            self.newTable.setRowCount(rows)
            self.newTable.setHorizontalHeaderLabels(header)
            self.newTable.setGeometry(QtCore.QRect(1, 0, 759, 349))
            self.newTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.newTable.horizontalHeader().setSectionResizeMode(3,QtWidgets.QHeaderView.Stretch)
            # if a row is double clicked then use showRowInfo function
            self.newTable.cellDoubleClicked.connect(self.showRowInfo)

            #insert values on table
            for row_num, row_data in enumerate(dataList):
                for col_num, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.newTable.setItem(row_num, col_num, item)
            
        # if there is´nt data initialize an empty widget
        else: self.newTable = QtWidgets.QTableWidget(MainWindow)

    def showRowInfo(self):
        code = 'Función en construcción'
        message = 'Función showPortsTableInfo en construcción'
        icon = QtWidgets.QMessageBox.Information
        self.errorMessage.showMessage(code, message, icon)