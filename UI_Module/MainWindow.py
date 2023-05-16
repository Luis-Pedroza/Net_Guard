# ***************************************************
# FILE: MainWindow.py
#
# DESCRIPTION: 
# -*- coding: utf-8 -*-
#
# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
#
# AUTHOR: Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

from PyQt5 import QtCore, QtGui, QtWidgets
from Controller_Module.Ports import Get_Data, Table_Counter
from Controller_Module.Scan import Scan_Ports
from Controller_Module.Rules import Firewall_Rules
from .UI_Scan_Tab import Ports_Range
from .UI_Rules_Tab import RulesTable_Creator
from .UI_Ports_Tab import Table_Creator
from .UI_Error import PopUp_Messages

class Ui_MainWindow(object):     
    def setupUi(self, MainWindow):     
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(755, 616)
        MainWindow.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 751, 571))
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setObjectName("tabWidget")

        #************************************************************
        #************************* TAB SCAN *************************
        #************************************************************
        self.tab_Scan = QtWidgets.QWidget()
        self.tab_Scan.setObjectName("tab_Scan")
        self.tabWidget.addTab(self.tab_Scan, "") 
        self.getList = Scan_Ports()

        #************************** Table ***************************"
        self.TableScan = QtWidgets.QTableWidget(self.tab_Scan)
        self.TableScan.setGeometry(QtCore.QRect(5, 0, 740, 445))
        self.TableScan.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TableScan.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.TableScan.setObjectName("TableScan")
        self.TableScan.setColumnCount(6)
        self.TableScan.cellDoubleClicked.connect(self.showScanTableInfo)
        
        item = QtWidgets.QTableWidgetItem()
        self.TableScan.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableScan.setHorizontalHeaderItem(1, item)
        self.TableScan.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.TableScan.setHorizontalHeaderItem(2, item)
        self.TableScan.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.TableScan.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableScan.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.TableScan.setHorizontalHeaderItem(5, item)

        #************************** Footer **************************"
        self.ScanPortsBtn = QtWidgets.QToolButton(self.tab_Scan)
        self.ScanPortsBtn.setGeometry(QtCore.QRect(20, 500, 101, 26))
        self.ScanPortsBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ScanPortsBtn.setObjectName("ScanPortsBtn")
        self.ScanPortsBtn.clicked.connect(lambda: self.updateScanTable(self.TableScan))
        
        self.labelRangeValueTCP = QtWidgets.QLabel(self.tab_Scan)
        self.labelRangeValueTCP.setGeometry(QtCore.QRect(190, 450, 58, 21))
        self.labelRangeValueTCP.setObjectName("labelRangeValueTCP")
        
        self.labelRangeTCP = QtWidgets.QLabel(self.tab_Scan)
        self.labelRangeTCP.setGeometry(QtCore.QRect(20, 450, 221, 21))
        self.labelRangeTCP.setObjectName("labelRangeTCP")
        
        self.EditRangeBtn = QtWidgets.QToolButton(self.tab_Scan)
        self.EditRangeBtn.setGeometry(QtCore.QRect(140, 500, 101, 26))
        self.EditRangeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.EditRangeBtn.setObjectName("EditRangeBtn")
        self.EditRangeBtn.clicked.connect(lambda: self.showPortsRangeWindow())
        
        self.labelRangeUDP = QtWidgets.QLabel(self.tab_Scan)
        self.labelRangeUDP.setGeometry(QtCore.QRect(20, 470, 221, 21))
        self.labelRangeUDP.setObjectName("labelRangeUDP")
        
        self.labelRangeValueUDP = QtWidgets.QLabel(self.tab_Scan)
        self.labelRangeValueUDP.setGeometry(QtCore.QRect(190, 470, 58, 21))
        self.labelRangeValueUDP.setObjectName("labelRangeValueUDP")

        self.updateScanTable(self.TableScan)

        #*************************************************************"
        #************************* TAB RULES *************************"
        #*************************************************************"
        self.tab_Rules = QtWidgets.QWidget()
        self.tab_Rules.setObjectName("tab_Rules")
        self.tabWidget.addTab(self.tab_Rules, "")
        self.getRules = Firewall_Rules()
        self.initNewRule = RulesTable_Creator()
        self.ruleWindow = QtWidgets.QWidget()

        #************************** Header ***************************"
        self.searchRuleBtn = QtWidgets.QToolButton(self.tab_Rules)

        self.labelRule = QtWidgets.QLabel(self.tab_Rules)
        self.labelRule.setGeometry(QtCore.QRect(30, 3, 58, 26))
        self.labelRule.setObjectName("labelRule")
        self.lineEditSearchRule = QtWidgets.QLineEdit(self.tab_Rules)
        self.lineEditSearchRule.setGeometry(QtCore.QRect(80, 4, 230, 20))
        self.lineEditSearchRule.setObjectName("lineEditSearchRule")
        self.lineEditSearchRule.returnPressed.connect(self.searchRuleBtn.click)

        self.labelProfile = QtWidgets.QLabel(self.tab_Rules)
        self.labelProfile.setGeometry(QtCore.QRect(350, 3, 80, 26))
        self.labelProfile.setObjectName("labelProfile")
        self.comboBoxProfileRule = QtWidgets.QComboBox(self.tab_Rules)
        self.comboBoxProfileRule.setGeometry(QtCore.QRect(380, 4, 80, 26))
        self.comboBoxProfileRule.setObjectName("comboBoxProfileRule")
        self.comboBoxProfileRule.addItem('Cualquiera')
        self.comboBoxProfileRule.addItem('Publico')
        self.comboBoxProfileRule.addItem('Privado')
        self.comboBoxProfileRule.addItem('Dominio')
        self.comboBoxProfileRule.setCurrentText('Cualquiera')
        
        self.labelDirection = QtWidgets.QLabel(self.tab_Rules)
        self.labelDirection.setGeometry(QtCore.QRect(475, 3, 80, 26))
        self.labelDirection.setObjectName("labelDirection")
        self.comboBoxDirectionRule = QtWidgets.QComboBox(self.tab_Rules)
        self.comboBoxDirectionRule.setGeometry(QtCore.QRect(525, 4, 76, 26))
        self.comboBoxDirectionRule.setObjectName("comboBoxDirectionRule")
        self.comboBoxDirectionRule.addItem('Cualquiera')
        self.comboBoxDirectionRule.addItem('Entrada')
        self.comboBoxDirectionRule.addItem('Salida')
        self.comboBoxDirectionRule.setCurrentText('Cualquiera')
        
        self.searchRuleBtn.setGeometry(QtCore.QRect(620, 4, 101, 26))
        self.searchRuleBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchRuleBtn.setObjectName("searchRuleBtn")
        self.searchRuleBtn.clicked.connect(self.showSearchRuleTable)
        

        #************************** Table ***************************"
        self.tableRules = QtWidgets.QTableWidget(self.tab_Rules)
        self.tableRules.setGeometry(QtCore.QRect(5, 35, 740, 447))
        self.tableRules.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableRules.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableRules.setObjectName("tableRules")
        self.tableRules.setColumnCount(6)
        self.tableRules.cellDoubleClicked.connect(self.showRulesWindowInfo)
        
        item = QtWidgets.QTableWidgetItem()
        self.tableRules.setVerticalHeaderItem(0, item)
        self.tableRules.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.tableRules.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableRules.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableRules.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableRules.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableRules.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableRules.setHorizontalHeaderItem(5, item)

        self.updateRulesTable(self.tableRules)
        
        #************************** Buttons ***************************"

        self.RefreshRuleBtn = QtWidgets.QToolButton(self.tab_Rules)
        self.RefreshRuleBtn.setGeometry(QtCore.QRect(150, 495, 101, 26))
        self.RefreshRuleBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.RefreshRuleBtn.setObjectName("RefreshRuleBtn")
        self.RefreshRuleBtn.clicked.connect(lambda: self.updateRulesTable(self.tableRules))

        self.NewRuleBtn = QtWidgets.QToolButton(self.tab_Rules)
        self.NewRuleBtn.setGeometry(QtCore.QRect(490, 495, 101, 26))
        self.NewRuleBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NewRuleBtn.setObjectName("NewRuleBtn")
        self.NewRuleBtn.clicked.connect(lambda: self.initNewRule.initRuleWindow(self.ruleWindow))

        #*************************************************************"
        #************************* TAB PORTS *************************"
        #*************************************************************"
        self.tab_Ports = QtWidgets.QWidget()
        self.tab_Ports.setObjectName("tab_Ports")
        self.tabWidget.addTab(self.tab_Ports, "")

        self.counter = Table_Counter(1,65535)
        self.updatedTable = Get_Data()
        self.errorMessage = PopUp_Messages()
        
        #************************** HEADER ***************************"
        self.SearchPortBtn = QtWidgets.QToolButton(self.tab_Ports)
        
        self.labelPort = QtWidgets.QLabel(self.tab_Ports)
        self.labelPort.setGeometry(QtCore.QRect(30, 4, 58, 26))
        self.labelPort.setObjectName("labelPort")
        self.spinBoxPort = QtWidgets.QSpinBox(self.tab_Ports)
        self.spinBoxPort.setGeometry(QtCore.QRect(77, 4, 75, 26))
        self.spinBoxPort.setMaximum(65535)
        self.spinBoxPort.setObjectName("spinBoxPort")

        self.labelService = QtWidgets.QLabel(self.tab_Ports)
        self.labelService.setGeometry(QtCore.QRect(170, 4, 51, 26))
        self.labelService.setObjectName("labelService")
        self.lineEditSearch = QtWidgets.QLineEdit(self.tab_Ports)
        self.lineEditSearch.setGeometry(QtCore.QRect(230, 4, 211, 26))
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.lineEditSearch.returnPressed.connect(self.SearchPortBtn.click)

        self.labelProtocol = QtWidgets.QLabel(self.tab_Ports)
        self.labelProtocol.setGeometry(QtCore.QRect(460, 4, 58, 26))
        self.labelProtocol.setObjectName("labelProtocol")
        self.comboBoxProtocol = QtWidgets.QComboBox(self.tab_Ports)
        self.comboBoxProtocol.setGeometry(QtCore.QRect(520, 4, 76, 26))
        self.comboBoxProtocol.setObjectName("comboBoxProtocol")
        self.comboBoxProtocol.addItem('Ambos')
        self.comboBoxProtocol.addItem('TCP')
        self.comboBoxProtocol.addItem('UDP')

        self.SearchPortBtn.setGeometry(QtCore.QRect(620, 4, 101, 26))
        self.SearchPortBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SearchPortBtn.setObjectName("SearchPortBtn")
        self.SearchPortBtn.clicked.connect(self.showSearchPortsTable)

        #*************************** TABLE ***************************"
        self.TablePorts = QtWidgets.QTableWidget(self.tab_Ports)
        self.TablePorts.setGeometry(QtCore.QRect(5, 35, 740, 447))
        self.TablePorts.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TablePorts.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.TablePorts.setObjectName("TablePorts")
        self.TablePorts.setColumnCount(5)
        self.TablePorts.setRowCount(14)
        self.TablePorts.cellDoubleClicked.connect(self.showPortsTableInfo)

        item = QtWidgets.QTableWidgetItem()
        self.TablePorts.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablePorts.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablePorts.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablePorts.setHorizontalHeaderItem(3, item)
        self.TablePorts.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.TablePorts.setHorizontalHeaderItem(4, item)

        self.updatePortsTable(self.TablePorts)
        
        #************************** BUTTONS **************************"
        self.PreviousTableBtn = QtWidgets.QToolButton(self.tab_Ports)
        self.PreviousTableBtn.setGeometry(QtCore.QRect(150, 495, 101, 26))
        self.PreviousTableBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PreviousTableBtn.setObjectName("PreviousTableBtn")
        self.PreviousTableBtn.clicked.connect(lambda: self.previousValue(self.TablePorts))
        
        self.NextTableBtn = QtWidgets.QToolButton(self.tab_Ports)
        self.NextTableBtn.setGeometry(QtCore.QRect(490, 495, 101, 26))
        self.NextTableBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NextTableBtn.setObjectName("NextTableBtn")
        self.NextTableBtn.clicked.connect(lambda: self.nextValue(self.TablePorts))
      
        
        #*************************************************************"
        #************************* MENU BAR **************************"
        #*************************************************************"
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 755, 22))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuConfig = QtWidgets.QMenu(self.menubar)
        self.menuConfig.setObjectName("menuConfig")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        MainWindow.setStatusBar(self.statusbar)
        self.action_New_Rule = QtWidgets.QAction(MainWindow)
        self.action_New_Rule.setObjectName("action_New_Rule")
        self.action_New_Rule.triggered.connect(lambda: self.initNewRule.initRuleWindow(self.ruleWindow))
        self.action_Change_Range = QtWidgets.QAction(MainWindow)
        self.action_Change_Range.setObjectName("action_Change_Range")
        self.action_Change_Range.triggered.connect(lambda: self.showPortsRangeWindow())

        self.helpChangeRange = QtWidgets.QAction(MainWindow)
        self.helpChangeRange.setObjectName("helpChangeRange")
        self.helpNewRule = QtWidgets.QAction(MainWindow)
        self.helpNewRule.setObjectName("helpNewRule")
        self.helpChangeRule = QtWidgets.QAction(MainWindow)
        self.helpChangeRule.setObjectName("helpChangeRule")
        self.helpSearchRule = QtWidgets.QAction(MainWindow)
        self.helpSearchRule.setObjectName("helpSearchRule")
        self.helpSearchPort = QtWidgets.QAction(MainWindow)
        self.helpSearchPort.setObjectName("helpSearchPort")
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")

        self.actionLanguage = QtWidgets.QAction(MainWindow)
        self.actionLanguage.setObjectName("actionLanguage")

        self.menuEdit.addAction(self.action_New_Rule)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.action_Change_Range)
        
        self.menuConfig.addAction(self.actionLanguage)
        self.menuHelp.addAction(self.helpChangeRange)
        self.menuHelp.addAction(self.helpNewRule)
        self.menuHelp.addAction(self.helpChangeRule)
        self.menuHelp.addAction(self.helpSearchRule)
        self.menuHelp.addAction(self.helpSearchPort)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.action_About)

        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Net Guard"))

        #************************************************************
        #************************* TAB SCAN *************************
        #************************************************************
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Scan), _translate("MainWindow", "Escáner"))

        item = self.TableScan.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Protocolo"))
        item = self.TableScan.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Dirección Local"))
        item = self.TableScan.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Dirección Remota"))
        item = self.TableScan.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Estado"))
        item = self.TableScan.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "PID"))
        item = self.TableScan.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Programa"))
            
        self.labelRangeTCP.setText(_translate("MainWindow", "Rango dinámico  de puertos TCP:"))
        self.labelRangeUDP.setText(_translate("MainWindow", "Rango dinámico  de puertos UDP:"))
        
        self.ScanPortsBtn.setText(_translate("MainWindow", "Actualizar"))
        self.EditRangeBtn.setText(_translate("MainWindow", "Modificar"))

        #************************************************************
        #************************* TAB RULES ************************
        #************************************************************
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Rules), _translate("MainWindow", "Reglas"))

        self.labelRule.setText(_translate("MainWindow", "Nombre"))
        self.labelProfile.setText(_translate("MainWindow", "Perfil"))
        self.labelDirection.setText(_translate("MainWindow", "Dirección"))
        self.searchRuleBtn.setText(_translate("MainWindow", "Buscar"))
        
        item = self.tableRules.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Regla"))
        item = self.tableRules.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Habilitada"))
        item = self.tableRules.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Perfil"))
        item = self.tableRules.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Acción"))
        item = self.tableRules.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Dirección"))
        item = self.tableRules.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Protocolo"))
        
        self.RefreshRuleBtn.setText(_translate("MainWindow", "Actualizar"))
        self.NewRuleBtn.setText(_translate("MainWindow", "Agregar"))

        #************************************************************
        #************************* TAB PORTS ************************
        #************************************************************
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Ports), _translate("MainWindow", "Puertos"))

        self.SearchPortBtn.setText(_translate("MainWindow", "Buscar"))
        self.labelPort.setText(_translate("MainWindow", "Puerto"))
        self.labelService.setText(_translate("MainWindow", "Servicio"))
        self.labelProtocol.setText(_translate("MainWindow", "Protocolo"))

        item = self.TablePorts.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Puerto"))
        item = self.TablePorts.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Servicio"))
        item = self.TablePorts.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Protocolo"))
        item = self.TablePorts.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Descripción"))
        item = self.TablePorts.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Referencia"))

        self.PreviousTableBtn.setText(_translate("MainWindow", "Atrás"))
        self.NextTableBtn.setText(_translate("MainWindow", "Siguiente"))

        #*************************************************************"
        #************************* MENU BAR **************************"
        #*************************************************************"
        
        self.menuEdit.setTitle(_translate("MainWindow", "Editar"))
        self.menuConfig.setTitle(_translate("MainWindow", "Configuración"))
        self.menuHelp.setTitle(_translate("MainWindow", "Ayuda"))
        
        self.action_New_Rule.setText(_translate("MainWindow", "Nueva Regla"))
        self.action_Change_Range.setText(_translate("MainWindow", "Cambiar rango de puertos"))

        self.actionLanguage.setText(_translate("MainWindow", "Idioma"))
        
        self.helpChangeRange.setText(_translate("MainWindow", "Cambiar rango de puertos"))
        self.helpNewRule.setText(_translate("MainWindow", "Crear nuevas reglas"))
        self.helpChangeRule.setText(_translate("MainWindow", "Modificar Reglas"))
        self.helpSearchRule.setText(_translate("MainWindow", "Buscar Reglas"))
        self.helpSearchPort.setText(_translate("MainWindow", "Buscar Puertos"))
        self.action_About.setText(_translate("MainWindow", "Acerca de Net Guard"))

    # Method to update the table in the scan tab.
    def updateScanTable(self, mainTable):
        #clear the table and get new values
        mainTable.clearContents()
        getData = self.getList.scanAll()
        #insert new values in table
        mainTable.setRowCount(len(getData))
        for row, row_data in enumerate(getData):
            for col, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                mainTable.setItem(row, col, item)
        #update table
        mainTable.repaint()

        #get Range of ports
        getRange = self.getList.getRange()
        tcpRange = getRange[0].splitlines()[4]
        udpRange = getRange[1].splitlines()[4]

        #set Range on labels
        self.labelRangeValueTCP.setText(tcpRange.split(':')[1])
        self.labelRangeValueUDP.setText(udpRange.split(':')[1])

    # Method to update the table in the rules tab
    # REVISAR BUG AL ACTUALIZAR SIN DATOS NUEVOS
    def updateRulesTable(self, mainTable):
        # Clear the table and get new values
        mainTable.clearContents()
        rules = self.getRules.showRules()
        # Insert new values on table
        mainTable.setRowCount(len(rules))
        for i, row in enumerate(rules):
            item = QtWidgets.QTableWidgetItem(str(row["Nombre de regla"]))
            mainTable.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem(str(row["Habilitada"]))
            mainTable.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem(str(row["Perfiles"]))
            mainTable.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem(str(row["Acción"]))
            mainTable.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem(str(row["Dirección"]))
            mainTable.setItem(i, 4, item)
            item = QtWidgets.QTableWidgetItem(str(row["Protocolo"]))
            mainTable.setItem(i, 5, item)
        # update table
        mainTable.repaint()
        
    # Method to update the table in the ports tab    
    def updatePortsTable(self, mainTable):
        # initialize maximum and minimum value of the counter to show only 14 values
        self.minValue = self.counter.current_value
        self.maxValue = self.counter.current_value + 13
        #get the ports by ID between minimum and maximum value
        self.newTable = self.updatedTable.get_all_ports(self.minValue, self.maxValue)
        #clear the table and insert new values
        if self.newTable:
            mainTable.clearContents()
            for row, row_data in enumerate(self.newTable):
                for col, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    mainTable.setItem(row, col, item)
            #update table
            mainTable.repaint()

    # Method to initialize the change of range window
    def showPortsRangeWindow(self):
        self.initRangeWindow = QtWidgets.QMainWindow()
        self.RangeWindow = Ports_Range()
        self.RangeWindow.setUpWindow(self.initRangeWindow)
        self.initRangeWindow.show()

    def showSearchRuleTable(self):
        icon = QtWidgets.QMessageBox.Information
        name = self.lineEditSearchRule.text()
        profile = self.comboBoxProfileRule.currentText()
        direction = self.comboBoxDirectionRule.currentText()
        self.InitSearchTable = QtWidgets.QMainWindow()

        translations = {
        "Cualquiera": "any",
        "Publico": "public",
        "Privado": "private",
        "Dominio": "domain",
        "Entrada": "in",
        "Salida": "out"
        }
        translateProfile = translations.get(profile, profile)
        translateDirection = translations.get(direction, direction)
        self.searchRule = RulesTable_Creator(name, translateProfile, translateDirection)
        self.searchRule.setupTable(self.InitSearchTable)

        if self.lineEditSearchRule.text() == '':
            code = 'Ingrese el nombre de la regla'
            error = 'Debe ingresar el nombre de la regla para poder realizar una búsqueda'
            self.errorMessage.showMessage(code, error, icon)
        elif self.searchRule.newTable.rowCount() == 0:
            code = 'No se encontraron datos coincidentes'
            error = 'La búsqueda no arrojo ningún dato coincidente con los parámetros ingresados'
            self.errorMessage.showMessage(code, error, icon)
        else: 
            self.InitSearchTable.show()
        self.lineEditSearchRule.clear()
        self.comboBoxProfileRule.setCurrentText('Cualquiera')
        self.comboBoxDirectionRule.setCurrentText('Cualquiera')


    # Method to show a table with the searched ports
    def showSearchPortsTable(self):
        #icon for the exception
        icon = QtWidgets.QMessageBox.Information
        #get the values
        port = self.spinBoxPort.value()
        service = self.lineEditSearch.text()
        protocol = self.comboBoxProtocol.currentText()

        #initialize new table with Table_Creator
        self.InitSearchTable = QtWidgets.QMainWindow()
        self.TableApp = Table_Creator(port, protocol, service)
        self.TableApp.setupTable(self.InitSearchTable)

        #exceptions of the search
        if port >= 49152:
            #port value is´nt registered 
            code = 'Puerto no registrado'
            error = 'El puerto que intenta buscar no se encuentra registrado por la IANA'
            self.errorMessage.showMessage(code, error, icon)
        elif service == '' and port == 0:
            #empty values of search
            code = 'No se puede realizar la búsqueda'
            error = 'La búsqueda no se puede procesar como la especifico, revise la ayuda para realizar búsquedas'
            self.errorMessage.showMessage(code, error, icon)
        elif self.TableApp.newTable.rowCount() == 0:
            #data is´nt on the DB
            code = 'No se encontraron datos coincidentes'
            error = 'La búsqueda no arrojo ningún dato coincidente con los parámetros ingresados'
            self.errorMessage.showMessage(code, error, icon)
        else:
            #show the results
            self.InitSearchTable.show()
        self.lineEditSearch.clear()
        self.spinBoxPort.setValue(0)
        self.comboBoxProtocol.setCurrentText('Ambos')
    
    #Method to show a windows with more information
    def showScanTableInfo(self):
        code = 'Función en construcción'
        message = 'Función showScanTableInfo en construcción'
        icon = QtWidgets.QMessageBox.Information
        self.errorMessage.showMessage(code, message, icon)

    def showRulesWindowInfo(self, row):
        translations = {
        "Pública": "public",
        "Privada": "private",
        "Dominio": "domain",
        }
        name = self.tableRules.item(row, 0).text()
        profile = self.tableRules.item(row,2).text()
        direction = self.tableRules.item(row,4).text()
        protocol = self.tableRules.item(row,5).text()
        
        direction = 'in' if direction == 'Dentro' else 'out'

        values = profile.split(",")
        # Traducir cada valor individualmente y unirlos en una cadena
        translated_values = [translations[value.strip()] if value.strip() in translations else value.strip() for value in values]
        translated_value = ",".join(translated_values)
        # Asignar el valor traducido a la variable profile
        profile = translated_value
        search = self.getRules.searchRules(name, profile, direction)
        self.initNewRule.initRuleWindow(self.ruleWindow, protocol, search, True)

    # Method to show a windows with more information
    def showPortsTableInfo(self):
        code = 'Función en construcción'
        message = 'Función showPortsTableInfo en construcción'
        icon = QtWidgets.QMessageBox.Information
        self.errorMessage.showMessage(code, message, icon)


    # counter to show the next 14 values on the table in the tab ports
    def nextValue(self, mainTable):
        self.counter.next()
        self.updatePortsTable(mainTable)
    # counter to show the previous 14 values on the table in the tab ports
    def previousValue(self, mainTable):
        self.counter.previous()
        self.updatePortsTable(mainTable)
    
