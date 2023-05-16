# ***************************************************
# FILE: UI_Ports_Tab.py
#
# DESCRIPTION: 
# This code creates a table with the data of the ports received 
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

        #initialize a new widget and a layout
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.layOut = QtWidgets.QVBoxLayout(self.centralWidget)

        # get the data from the DB through the function get_search
        dataList = self.data_table_ports.get_search(self.port, self.protocol, self.service)

        # if there´s data
        if dataList:
            # get number of rows
            rows = len(dataList)
            # initialize widget with the specifications 
            self.newTable = QtWidgets.QTableWidget(self.centralWidget)
            header = ['Puerto', 'Servicio', 'Protocolo', 'Descripción', 'Referencia' ]
            self.newTable.setColumnCount(5)
            self.newTable.setRowCount(rows)
            self.newTable.setHorizontalHeaderLabels(header)
            self.newTable.setGeometry(QtCore.QRect(1, 0, 759, 511))
            self.newTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.newTable.horizontalHeader().setSectionResizeMode(3,QtWidgets.QHeaderView.Stretch)
            # if a row is double clicked then use showRowInfo function
            self.newTable.cellDoubleClicked.connect(self.showRowInfo)

            #insert values on table
            for row_num, row_data in enumerate(dataList):
                for col_num, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    self.newTable.setItem(row_num, col_num, item)

            #add the table to the layout    
            self.layOut.addWidget(self.newTable)
            self.scrollArea = QtWidgets.QScrollArea()
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setWidget(self.centralWidget)

            # set the scroll Area on the MainWindow
            MainWindow.setCentralWidget(self.scrollArea)
            
        # if there is´nt data initialize an empty widget
        else: self.newTable = QtWidgets.QTableWidget(self.centralWidget)

    def showRowInfo(self):
        code = 'Función en construcción'
        message = 'Función showPortsTableInfo en construcción'
        icon = QtWidgets.QMessageBox.Information
        self.errorMessage.showMessage(code, message, icon)
        
            
        
        
        
        
        

        

        

        

