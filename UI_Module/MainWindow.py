# ***************************************************
# FILE: MainWindow.py
#
# -*- coding: utf-8 -*-
# DESCRIPTION: 
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
from Controller_Module.Rules import Firewall_Rules
from Controller_Module.Report import Report_PDF
from Controller_Module.Scan import Scan_Ports
from .UI_Rules_Tab import RulesTableCreator
from .UI_Ports_Tab import Table_Creator
from .UI_Scan_Tab import Ports_Range
from .UI_Error import PopUp_Messages
from .UI_About import Ui_Dialog

class Ui_MainWindow(object):     
    def setupUi(self, MainWindow):  
        self.saveReport = Report_PDF()
        path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation) + "/Reporte.pdf"
   
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(755, 616)
        MainWindow.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)

        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setEnabled(True)
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
        self.TableScan.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TableScan.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.TableScan.setObjectName("TableScan")
        self.TableScan.setColumnCount(6)
        self.TableScan.cellDoubleClicked.connect(self.showScanTableInfo)
        self.TableScan.horizontalHeader().sectionClicked.connect(lambda col: self.sort_table(self.TableScan, col))
        
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
        
        self.labelRangeTCP = QtWidgets.QLabel(self.tab_Scan)
        self.labelRangeTCP.setObjectName("labelRangeTCP")
        self.labelRangeValueTCP = QtWidgets.QLabel(self.tab_Scan)
        self.labelRangeValueTCP.setObjectName("labelRangeValueTCP")
        
        self.labelRangeUDP = QtWidgets.QLabel(self.tab_Scan)
        self.labelRangeUDP.setObjectName("labelRangeUDP")
        self.labelRangeValueUDP = QtWidgets.QLabel(self.tab_Scan)
        self.labelRangeValueUDP.setObjectName("labelRangeValueUDP")

        self.updateScanTable(self.TableScan)

        self.ScanPortsBtn = QtWidgets.QToolButton(self.tab_Scan)
        self.ScanPortsBtn.setFixedSize(101, 26)
        self.ScanPortsBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ScanPortsBtn.setObjectName("ScanPortsBtn")
        self.ScanPortsBtn.clicked.connect(lambda: self.updateScanTable(self.TableScan))

        self.EditRangeBtn = QtWidgets.QToolButton(self.tab_Scan)
        self.EditRangeBtn.setFixedSize(101, 26)
        self.EditRangeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.EditRangeBtn.setObjectName("EditRangeBtn")
        self.EditRangeBtn.clicked.connect(lambda: self.showPortsRangeWindow())

        self.TableScanLayout = QtWidgets.QGridLayout(self.tab_Scan)
        self.TableScanLayout.addWidget(self.TableScan, 0, 0, 1, 3)
        self.TableScanLayout.addWidget(self.labelRangeTCP, 1, 0)
        self.TableScanLayout.addWidget(self.labelRangeValueTCP, 1, 1)
        self.TableScanLayout.addWidget(self.labelRangeUDP, 2, 0)
        self.TableScanLayout.addWidget(self.labelRangeValueUDP, 2, 1)
        self.TableScanLayout.addWidget(self.ScanPortsBtn, 3, 0)
        self.TableScanLayout.addWidget(self.EditRangeBtn, 3, 1)


        #*************************************************************"
        #************************* TAB RULES *************************"
        #*************************************************************"
        self.tab_Rules = QtWidgets.QWidget()
        self.tab_Rules.setObjectName("tab_Rules")
        self.tabWidget.addTab(self.tab_Rules, "")
        self.getRules = Firewall_Rules()
        self.initRuleWindow = QtWidgets.QDialog()
        self.initNewRule = RulesTableCreator()

        #************************** Header ***************************"
        self.searchRuleBtn = QtWidgets.QToolButton(self.tab_Rules)

        self.labelRule = QtWidgets.QLabel(self.tab_Rules)
        self.labelRule.setObjectName("labelRule")
        self.lineEditSearchRule = QtWidgets.QLineEdit(self.tab_Rules)
        self.lineEditSearchRule.setObjectName("lineEditSearchRule")
        self.lineEditSearchRule.returnPressed.connect(self.searchRuleBtn.click)

        self.labelProfile = QtWidgets.QLabel(self.tab_Rules)
        self.labelProfile.setObjectName("labelProfile")
        self.comboBoxProfileRule = QtWidgets.QComboBox(self.tab_Rules)
        self.comboBoxProfileRule.setObjectName("comboBoxProfileRule")
        self.comboBoxProfileRule.addItem('Cualquiera')
        self.comboBoxProfileRule.addItem('Publico')
        self.comboBoxProfileRule.addItem('Privado')
        self.comboBoxProfileRule.addItem('Dominio')
        self.comboBoxProfileRule.setCurrentText('Cualquiera')
        
        self.labelDirection = QtWidgets.QLabel(self.tab_Rules)
        self.labelDirection.setObjectName("labelDirection")
        self.comboBoxDirectionRule = QtWidgets.QComboBox(self.tab_Rules)
        self.comboBoxDirectionRule.setObjectName("comboBoxDirectionRule")
        self.comboBoxDirectionRule.addItem('Cualquiera')
        self.comboBoxDirectionRule.addItem('Entrada')
        self.comboBoxDirectionRule.addItem('Salida')
        self.comboBoxDirectionRule.setCurrentText('Cualquiera')
        
        self.searchRuleBtn.setFixedSize(101, 26)
        self.searchRuleBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchRuleBtn.setObjectName("searchRuleBtn")
        self.searchRuleBtn.clicked.connect(self.showSearchRuleTable)
        

        #************************** Table ***************************"
        self.tableRules = QtWidgets.QTableWidget(self.tab_Rules)
        self.tableRules.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableRules.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableRules.setObjectName("tableRules")
        self.tableRules.setColumnCount(6)
        self.tableRules.cellDoubleClicked.connect(self.showRulesWindowInfo)
        self.tableRules.horizontalHeader().sectionClicked.connect(lambda col: self.sort_table(self.tableRules, col))
        
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
        self.RefreshRuleBtn.setFixedSize(101, 26)
        self.RefreshRuleBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.RefreshRuleBtn.setObjectName("RefreshRuleBtn")
        self.RefreshRuleBtn.clicked.connect(lambda: self.updateRulesTable(self.tableRules))

        self.NewRuleBtn = QtWidgets.QToolButton(self.tab_Rules)
        self.NewRuleBtn.setFixedSize(101, 26)
        self.NewRuleBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NewRuleBtn.setObjectName("NewRuleBtn")
        self.NewRuleBtn.clicked.connect(lambda: self.show_new_rule_window())

        self.TableRulesLayout = QtWidgets.QGridLayout(self.tab_Rules)
        self.TableRulesLayout.addWidget(self.labelRule, 0,0)
        self.TableRulesLayout.addWidget(self.lineEditSearchRule, 0,1)
        self.TableRulesLayout.addWidget(self.labelProfile, 0,2)
        self.TableRulesLayout.addWidget(self.comboBoxProfileRule, 0,3)
        self.TableRulesLayout.addWidget(self.labelDirection, 0,4)
        self.TableRulesLayout.addWidget(self.comboBoxDirectionRule, 0,5)
        self.TableRulesLayout.addWidget(self.searchRuleBtn, 0,6)
        self.TableRulesLayout.addWidget(self.tableRules, 1, 0, 1, 7)
        self.TableRulesLayout.addWidget(self.RefreshRuleBtn, 2,0)
        self.TableRulesLayout.addWidget(self.NewRuleBtn, 2,1)

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
        self.labelPort.setObjectName("labelPort")
        self.spinBoxPort = QtWidgets.QSpinBox(self.tab_Ports)
        self.spinBoxPort.setMaximum(65535)
        self.spinBoxPort.setObjectName("spinBoxPort")

        self.labelService = QtWidgets.QLabel(self.tab_Ports)
        self.labelService.setObjectName("labelService")
        self.lineEditSearch = QtWidgets.QLineEdit(self.tab_Ports)
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.lineEditSearch.returnPressed.connect(self.SearchPortBtn.click)

        self.labelProtocol = QtWidgets.QLabel(self.tab_Ports)
        self.labelProtocol.setObjectName("labelProtocol")
        self.comboBoxProtocol = QtWidgets.QComboBox(self.tab_Ports)
        self.comboBoxProtocol.setObjectName("comboBoxProtocol")
        self.comboBoxProtocol.addItem('Ambos')
        self.comboBoxProtocol.addItem('TCP')
        self.comboBoxProtocol.addItem('UDP')

        self.SearchPortBtn.setFixedSize(101, 26)
        self.SearchPortBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SearchPortBtn.setObjectName("SearchPortBtn")
        self.SearchPortBtn.clicked.connect(self.showSearchPortsTable)

        #*************************** TABLE ***************************"
        self.TablePorts = QtWidgets.QTableWidget(self.tab_Ports)
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
        self.PreviousTableBtn.setFixedSize(101, 26)
        self.PreviousTableBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PreviousTableBtn.setObjectName("PreviousTableBtn")
        self.PreviousTableBtn.clicked.connect(lambda: self.previousValue(self.TablePorts))
        
        self.NextTableBtn = QtWidgets.QToolButton(self.tab_Ports)
        self.NextTableBtn.setFixedSize(101, 26)
        self.NextTableBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NextTableBtn.setObjectName("NextTableBtn")
        self.NextTableBtn.clicked.connect(lambda: self.nextValue(self.TablePorts))
      
        self.TablePortsLayout = QtWidgets.QGridLayout(self.tab_Ports)
        self.TablePortsLayout.addWidget(self.labelPort, 0, 0)
        self.TablePortsLayout.addWidget(self.spinBoxPort, 0, 1)
        self.TablePortsLayout.addWidget(self.labelService, 0, 2)
        self.TablePortsLayout.addWidget(self.lineEditSearch, 0, 3)
        self.TablePortsLayout.addWidget(self.labelProtocol, 0, 4)
        self.TablePortsLayout.addWidget(self.comboBoxProtocol, 0, 5)
        self.TablePortsLayout.addWidget(self.SearchPortBtn, 0, 6)
        self.TablePortsLayout.addWidget(self.TablePorts, 1, 0, 1, 7)
        self.TablePortsLayout.addWidget(self.PreviousTableBtn, 2, 0)
        self.TablePortsLayout.addWidget(self.NextTableBtn, 2, 1)
        
        #*************************************************************"
        #************************* MENU BAR **************************"
        #*************************************************************"
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 755, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
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
        
        #************************** FILE **************************"
        self.action_Save_Scan = QtWidgets.QAction(MainWindow)
        self.action_Save_Scan.setShortcut('Ctrl+S')
        self.action_Save_Scan.setObjectName("action_Save_Scan")
        self.action_Save_Scan.triggered.connect(lambda: self.saveReport.saveToPDF(path, self.TableScan, True))
        self.action_Save_Rules = QtWidgets.QAction(MainWindow)
        self.action_Save_Rules.setShortcut('Ctrl+R')
        self.action_Save_Rules.setObjectName("action_Save_Rules")
        self.action_Save_Rules.triggered.connect(lambda: self.saveReport.saveToPDF(path, self.tableRules, False))
        

        #************************** EDIT **************************"
        self.action_New_Rule = QtWidgets.QAction(MainWindow)
        self.action_New_Rule.setShortcut('Ctrl+N')
        self.action_New_Rule.setObjectName("action_New_Rule")
        self.action_New_Rule.triggered.connect(lambda: self.show_new_rule_window())
        self.action_Change_Range = QtWidgets.QAction(MainWindow)
        self.action_Change_Range.setShortcut('Ctrl+C')
        self.action_Change_Range.setObjectName("action_Change_Range")
        self.action_Change_Range.triggered.connect(lambda: self.showPortsRangeWindow())
        self.action_Refresh_Scan = QtWidgets.QAction(MainWindow)
        self.action_Refresh_Scan.setShortcut('Ctrl+E')
        self.action_Refresh_Scan.setObjectName("action_Refresh_Scan")
        self.action_Refresh_Scan.triggered.connect(lambda: self.updateScanTable(self.TableScan))

        #************************** CONFIG **************************"
        self.actionLanguage = QtWidgets.QAction(MainWindow)
        self.actionLanguage.setObjectName("actionLanguage")
        self.actionLanguage.setShortcut('Ctrl+L')
        self.actionTheme = QtWidgets.QAction(MainWindow)
        self.actionTheme.setObjectName("actionTheme")
        self.actionTheme.setShortcut('Ctrl+T')

        #************************** HELP **************************"
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
        self.action_About.triggered.connect(lambda: self.openAbout())

        self.menuFile.addAction(self.action_Save_Scan)
        self.menuFile.addAction(self.action_Save_Rules)

        self.menuEdit.addAction(self.action_New_Rule)
        self.menuEdit.addAction(self.action_Change_Range)
        self.menuEdit.addAction(self.action_Refresh_Scan)
        
        self.menuConfig.addAction(self.actionLanguage)
        self.menuConfig.addAction(self.actionTheme)

        self.menuHelp.addAction(self.helpChangeRange)
        self.menuHelp.addAction(self.helpNewRule)
        self.menuHelp.addAction(self.helpChangeRule)
        self.menuHelp.addAction(self.helpSearchRule)
        self.menuHelp.addAction(self.helpSearchPort)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.action_About)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.tabWidget.setCurrentIndex(0)
        self.mainLayout.addWidget(self.tabWidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.translator = QtCore.QTranslator()
        self.translator.load("Resources/lan/language_en.qm")
        QtCore.QCoreApplication.installTranslator(self.translator)
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
            
        self.labelRangeTCP.setText(_translate("MainWindow", "Rango TCP:"))
        self.labelRangeUDP.setText(_translate("MainWindow", "Rango UDP:"))
        
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
        
        self.menuFile.setTitle(_translate("MainWindow", "Archivo"))
        self.menuEdit.setTitle(_translate("MainWindow", "Editar"))
        self.menuConfig.setTitle(_translate("MainWindow", "Configuración"))
        self.menuHelp.setTitle(_translate("MainWindow", "Ayuda"))

        self.action_Save_Scan.setText(_translate("MainWindow", "Guardar Escaneo"))
        self.action_Save_Rules.setText(_translate("MainWindow", "Guardar Reglas"))
        
        self.action_New_Rule.setText(_translate("MainWindow", "Nueva Regla"))
        self.action_Change_Range.setText(_translate("MainWindow", "Cambiar Rango de Puertos"))
        self.action_Refresh_Scan.setText(_translate("MainWindow", "Actualizar Escaneo"))

        self.actionLanguage.setText(_translate("MainWindow", "Idioma"))
        self.actionTheme.setText(_translate("MainWindow", "Tema"))
        
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
        mainTable.setRowCount(0)
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
    def updateRulesTable(self, mainTable):
        # Clear the table and get new values
        mainTable.clearContents()
        mainTable.setRowCount(0)
        rules = self.getRules.showRules()
        # Insert new values on table
        mainTable.setRowCount(len(rules))
        for i, row in enumerate(rules):
            item = QtWidgets.QTableWidgetItem(str(row["Name"]))
            mainTable.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem(str(row["Enabled"]))
            mainTable.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem(", ".join(row["Profiles"]))
            mainTable.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem(str(row["Action"]))
            mainTable.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem(str(row["Direction"]))
            mainTable.setItem(i, 4, item)
            item = QtWidgets.QTableWidgetItem(str(row["Protocol"]))
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
        # Method to sort table
    def sort_table(self, table, column):
        table.sortItems(column, QtCore.Qt.AscendingOrder)

    # Method to initialize the change of range window
    def showPortsRangeWindow(self):
        self.initRangeWindow = QtWidgets.QDialog()
        self.RangeWindow = Ports_Range()
        self.RangeWindow.setUpWindow(self.initRangeWindow)
        self.initRangeWindow.exec_()

    def showSearchRuleTable(self):
        icon = QtWidgets.QMessageBox.Information
        name = self.lineEditSearchRule.text()
        profile = self.comboBoxProfileRule.currentText()
        direction = self.comboBoxDirectionRule.currentText()
        self.InitSearchTable = QtWidgets.QDialog()

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
        self.searchRule = RulesTableCreator(name, translateProfile, translateDirection)
        self.searchRule.setup_rules_table(self.InitSearchTable)

        if self.lineEditSearchRule.text() == '':
            code = 'Ingrese el nombre de la regla'
            error = 'Debe ingresar el nombre de la regla para poder realizar una búsqueda'
            self.errorMessage.showMessage(code, error, icon)
        elif self.searchRule.newTable.rowCount() == 0:
            code = 'No se encontraron datos coincidentes'
            error = 'La búsqueda no arrojo ningún dato coincidente con los parámetros ingresados'
            self.errorMessage.showMessage(code, error, icon)
        else: 
            self.InitSearchTable.exec_()
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
        self.InitSearchTable = QtWidgets.QDialog()
        self.TableApp = Table_Creator(port, protocol, service)
        self.TableApp.setup_rules_table(self.InitSearchTable)

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
            error = 'La búsqueda no arrojó ningún dato coincidente con los parámetros ingresados'
            self.errorMessage.showMessage(code, error, icon)
        else:
            #show the results
            self.InitSearchTable.exec_()
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
        self.initNewRule.init_rule_window(self.initRuleWindow, protocol, search, True)
        self.initRuleWindow.exec_()

    def show_new_rule_window(self):
        self.init_rules_dialog = QtWidgets.QDialog()
        self.RuleWindow = RulesTableCreator()
        self.RuleWindow.init_rule_window(self.init_rules_dialog)
        self.init_rules_dialog.exec_()

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
    
    def openAbout(self):
        about_dialog = QtWidgets.QDialog()
        ui_about = Ui_Dialog()
        ui_about.setupUi(about_dialog)
        about_dialog.exec_()