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
from Controller.Ports import GetPortsData, TableCounter
from Controller.Rules import FirewallManager
from Controller.Report import ReportPDF
from Controller.Scan import ScanPorts
from .RulesTab import RulesTableCreator
from .PortsTab import TablePortsCreator
from .ScanTab import PortsRangeWindow
from .Alerts import PopUpMessage
from .About import UiDialog

class Ui_MainWindow(object):     
    def setupUi(self, main_window):  
        self.report_manager = ReportPDF()
        report_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
   
        main_window.setObjectName("main_window")
        main_window.resize(755, 616)
        main_window.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.tabWidget = QtWidgets.QTabWidget(self.central_widget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setObjectName("tabWidget")

        #************************************************************
        #************************* TAB SCAN *************************
        #************************************************************
        self.tab_Scan = QtWidgets.QWidget()
        self.tab_Scan.setObjectName("tab_Scan")
        self.tabWidget.addTab(self.tab_Scan, "") 
        self.connection_manager = ScanPorts()

        #************************** Table ***************************"
        self.scan_table = QtWidgets.QTableWidget(self.tab_Scan)
        self.scan_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.scan_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.scan_table.setObjectName("scan_table")
        self.scan_table.setColumnCount(6)
        self.scan_table.cellDoubleClicked.connect(self.showScanTableInfo)
        self.scan_table.horizontalHeader().sectionClicked.connect(lambda col: self.sort_table(self.scan_table, col))
        
        item = QtWidgets.QTableWidgetItem()
        self.scan_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.scan_table.setHorizontalHeaderItem(1, item)
        self.scan_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.scan_table.setHorizontalHeaderItem(2, item)
        self.scan_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.scan_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.scan_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.scan_table.setHorizontalHeaderItem(5, item)

        #************************** Footer **************************"
        
        self.label_rangeTCP = QtWidgets.QLabel(self.tab_Scan)
        self.label_rangeTCP.setObjectName("label_rangeTCP")
        self.label_valueTCP = QtWidgets.QLabel(self.tab_Scan)
        self.label_valueTCP.setObjectName("label_valueTCP")
        
        self.label_rangeUDP = QtWidgets.QLabel(self.tab_Scan)
        self.label_rangeUDP.setObjectName("label_rangeUDP")
        self.label_valueUDP = QtWidgets.QLabel(self.tab_Scan)
        self.label_valueUDP.setObjectName("label_valueUDP")

        self.updateScanTable(self.scan_table)

        self.port_scan_btn = QtWidgets.QToolButton(self.tab_Scan)
        self.port_scan_btn.setFixedSize(101, 26)
        self.port_scan_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.port_scan_btn.setObjectName("port_scan_btn")
        self.port_scan_btn.clicked.connect(lambda: self.updateScanTable(self.scan_table))

        self.edit_range_btn = QtWidgets.QToolButton(self.tab_Scan)
        self.edit_range_btn.setFixedSize(101, 26)
        self.edit_range_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_range_btn.setObjectName("edit_range_btn")
        self.edit_range_btn.clicked.connect(lambda: self.showPortsRangeWindow())

        self.scan_table_layout = QtWidgets.QGridLayout(self.tab_Scan)
        self.scan_table_layout.addWidget(self.scan_table, 0, 0, 1, 3)
        self.scan_table_layout.addWidget(self.label_rangeTCP, 1, 0)
        self.scan_table_layout.addWidget(self.label_valueTCP, 1, 1)
        self.scan_table_layout.addWidget(self.label_rangeUDP, 2, 0)
        self.scan_table_layout.addWidget(self.label_valueUDP, 2, 1)
        self.scan_table_layout.addWidget(self.port_scan_btn, 3, 0)
        self.scan_table_layout.addWidget(self.edit_range_btn, 3, 1)


        #*************************************************************"
        #************************* TAB RULES *************************"
        #*************************************************************"
        self.tab_Rules = QtWidgets.QWidget()
        self.tab_Rules.setObjectName("tab_Rules")
        self.tabWidget.addTab(self.tab_Rules, "")
        self.rules_manager = FirewallManager()
        self.get_searched_rules = RulesTableCreator()

        #************************** Header ***************************"
        self.search_rule_btn = QtWidgets.QToolButton(self.tab_Rules)

        self.label_rule = QtWidgets.QLabel(self.tab_Rules)
        self.label_rule.setObjectName("label_rule")
        self.lineEdit_search_rule = QtWidgets.QLineEdit(self.tab_Rules)
        self.lineEdit_search_rule.setObjectName("lineEdit_search_rule")
        self.lineEdit_search_rule.returnPressed.connect(self.search_rule_btn.click)

        self.label_profile = QtWidgets.QLabel(self.tab_Rules)
        self.label_profile.setObjectName("label_profile")
        self.comboBox_rule_profile = QtWidgets.QComboBox(self.tab_Rules)
        self.comboBox_rule_profile.setObjectName("comboBox_rule_profile")
        
        self.label_direction = QtWidgets.QLabel(self.tab_Rules)
        self.label_direction.setObjectName("label_direction")
        self.comboBox_rule_direction = QtWidgets.QComboBox(self.tab_Rules)
        self.comboBox_rule_direction.setObjectName("comboBox_rule_direction")
        self.comboBox_rule_direction.addItem('Any')
        self.comboBox_rule_direction.addItem('Inbound')
        self.comboBox_rule_direction.addItem('Outbound')
        
        self.search_rule_btn.setFixedSize(101, 26)
        self.search_rule_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_rule_btn.setObjectName("search_rule_btn")
        self.search_rule_btn.clicked.connect(self.showSearchRuleTable)
        

        #************************** Table ***************************"
        self.rules_table = QtWidgets.QTableWidget(self.tab_Rules)
        self.rules_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.rules_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.rules_table.setObjectName("rules_table")
        self.rules_table.setColumnCount(6)
        self.rules_table.cellDoubleClicked.connect(lambda row: self.get_searched_rules.get_selected_rule(self.rules_table, row))
        self.rules_table.cellDoubleClicked.connect(lambda: self.updateRulesTable(self.rules_table))
        self.rules_table.horizontalHeader().sectionClicked.connect(lambda col: self.sort_table(self.rules_table, col))
        
        item = QtWidgets.QTableWidgetItem()
        self.rules_table.setVerticalHeaderItem(0, item)
        self.rules_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.rules_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.rules_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.rules_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.rules_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.rules_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.rules_table.setHorizontalHeaderItem(5, item)

        self.updateRulesTable(self.rules_table)
        
        #************************** Buttons ***************************"
        self.reload_rules_table = QtWidgets.QToolButton(self.tab_Rules)
        self.reload_rules_table.setFixedSize(101, 26)
        self.reload_rules_table.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reload_rules_table.setObjectName("reload_rules_table")
        self.reload_rules_table.clicked.connect(lambda: self.updateRulesTable(self.rules_table))

        self.new_rule_btn = QtWidgets.QToolButton(self.tab_Rules)
        self.new_rule_btn.setFixedSize(101, 26)
        self.new_rule_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.new_rule_btn.setObjectName("new_rule_btn")
        self.new_rule_btn.clicked.connect(lambda: self.show_new_rule_window())
        self.new_rule_btn.clicked.connect(lambda: self.updateRulesTable(self.rules_table))

        self.rules_table_layout = QtWidgets.QGridLayout(self.tab_Rules)
        self.rules_table_layout.addWidget(self.label_rule, 0,0)
        self.rules_table_layout.addWidget(self.lineEdit_search_rule, 0,1)
        self.rules_table_layout.addWidget(self.label_profile, 0,2)
        self.rules_table_layout.addWidget(self.comboBox_rule_profile, 0,3)
        self.rules_table_layout.addWidget(self.label_direction, 0,4)
        self.rules_table_layout.addWidget(self.comboBox_rule_direction, 0,5)
        self.rules_table_layout.addWidget(self.search_rule_btn, 0,6)
        self.rules_table_layout.addWidget(self.rules_table, 1, 0, 1, 7)
        self.rules_table_layout.addWidget(self.reload_rules_table, 2,0)
        self.rules_table_layout.addWidget(self.new_rule_btn, 2,1)

        #*************************************************************"
        #************************* TAB PORTS *************************"
        #*************************************************************"
        self.tab_Ports = QtWidgets.QWidget()
        self.tab_Ports.setObjectName("tab_Ports")
        self.tabWidget.addTab(self.tab_Ports, "")

        self.counter = TableCounter(1,65535)
        self.ports_manager = GetPortsData()
        self.messages_manager = PopUpMessage()
        
        #************************** HEADER ***************************"
        self.search_port_btn = QtWidgets.QToolButton(self.tab_Ports)
        
        self.label_port = QtWidgets.QLabel(self.tab_Ports)
        self.label_port.setObjectName("label_port")
        self.spinBox_port = QtWidgets.QSpinBox(self.tab_Ports)
        self.spinBox_port.setMaximum(65535)
        self.spinBox_port.setObjectName("spinBox_port")

        self.label_service = QtWidgets.QLabel(self.tab_Ports)
        self.label_service.setObjectName("label_service")
        self.lineEdit_search = QtWidgets.QLineEdit(self.tab_Ports)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.lineEdit_search.returnPressed.connect(self.search_port_btn.click)

        self.label_protocol = QtWidgets.QLabel(self.tab_Ports)
        self.label_protocol.setObjectName("label_protocol")
        self.comboBox_protocol = QtWidgets.QComboBox(self.tab_Ports)
        self.comboBox_protocol.setObjectName("comboBox_protocol")

        self.search_port_btn.setFixedSize(101, 26)
        self.search_port_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_port_btn.setObjectName("search_port_btn")
        self.search_port_btn.clicked.connect(self.showSearchPortsTable)

        #*************************** TABLE ***************************"
        self.ports_table = QtWidgets.QTableWidget(self.tab_Ports)
        self.ports_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ports_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ports_table.setObjectName("ports_table")
        self.ports_table.setColumnCount(5)
        self.ports_table.setRowCount(14)
        self.ports_table.cellDoubleClicked.connect(self.showPortsTableInfo)

        item = QtWidgets.QTableWidgetItem()
        self.ports_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ports_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ports_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ports_table.setHorizontalHeaderItem(3, item)
        self.ports_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.ports_table.setHorizontalHeaderItem(4, item)

        self.updatePortsTable(self.ports_table)
        
        #************************** BUTTONS **************************"
        self.previous_table_btn = QtWidgets.QToolButton(self.tab_Ports)
        self.previous_table_btn.setFixedSize(101, 26)
        self.previous_table_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.previous_table_btn.setObjectName("previous_table_btn")
        self.previous_table_btn.clicked.connect(lambda: self.previousValue(self.ports_table))
        
        self.next_table_btn = QtWidgets.QToolButton(self.tab_Ports)
        self.next_table_btn.setFixedSize(101, 26)
        self.next_table_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next_table_btn.setObjectName("next_table_btn")
        self.next_table_btn.clicked.connect(lambda: self.nextValue(self.ports_table))
      
        self.ports_table_layout = QtWidgets.QGridLayout(self.tab_Ports)
        self.ports_table_layout.addWidget(self.label_port, 0, 0)
        self.ports_table_layout.addWidget(self.spinBox_port, 0, 1)
        self.ports_table_layout.addWidget(self.label_service, 0, 2)
        self.ports_table_layout.addWidget(self.lineEdit_search, 0, 3)
        self.ports_table_layout.addWidget(self.label_protocol, 0, 4)
        self.ports_table_layout.addWidget(self.comboBox_protocol, 0, 5)
        self.ports_table_layout.addWidget(self.search_port_btn, 0, 6)
        self.ports_table_layout.addWidget(self.ports_table, 1, 0, 1, 7)
        self.ports_table_layout.addWidget(self.previous_table_btn, 2, 0)
        self.ports_table_layout.addWidget(self.next_table_btn, 2, 1)
        
        #*************************************************************"
        #************************* MENU BAR **************************"
        #*************************************************************"
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 755, 22))
        self.menu_bar.setObjectName("menu_bar")
        self.file_menu = QtWidgets.QMenu(self.menu_bar)
        self.file_menu.setObjectName("file_menu")
        self.edit_menu = QtWidgets.QMenu(self.menu_bar)
        self.edit_menu.setObjectName("edit_menu")
        self.config_menu = QtWidgets.QMenu(self.menu_bar)
        self.config_menu.setObjectName("config_menu")
        self.help_menu = QtWidgets.QMenu(self.menu_bar)
        self.help_menu.setObjectName("help_menu")
        
        main_window.setMenuBar(self.menu_bar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        
        #************************** FILE **************************"
        self.action_save_scan = QtWidgets.QAction(main_window)
        self.action_save_scan.setShortcut('Ctrl+S')
        self.action_save_scan.setObjectName("action_save_scan")
        self.action_save_scan.triggered.connect(lambda: self.report_manager.save_to_PDF(report_path, self.scan_table, True))
        self.action_save_rules = QtWidgets.QAction(main_window)
        self.action_save_rules.setShortcut('Ctrl+R')
        self.action_save_rules.setObjectName("action_save_rules")
        self.action_save_rules.triggered.connect(lambda: self.report_manager.save_to_PDF(report_path, self.rules_table, False))
        

        #************************** EDIT **************************"
        self.action_new_rule = QtWidgets.QAction(main_window)
        self.action_new_rule.setShortcut('Ctrl+N')
        self.action_new_rule.setObjectName("action_new_rule")
        self.action_new_rule.triggered.connect(lambda: self.show_new_rule_window())
        self.action_change_range = QtWidgets.QAction(main_window)
        self.action_change_range.setShortcut('Ctrl+C')
        self.action_change_range.setObjectName("action_change_range")
        self.action_change_range.triggered.connect(lambda: self.showPortsRangeWindow())
        self.action_reload_scan = QtWidgets.QAction(main_window)
        self.action_reload_scan.setShortcut('Ctrl+E')
        self.action_reload_scan.setObjectName("action_reload_scan")
        self.action_reload_scan.triggered.connect(lambda: self.updateScanTable(self.scan_table))

        #************************** CONFIG **************************"
        self.action_select_language = QtWidgets.QAction(main_window)
        self.action_select_language.setObjectName("action_select_language")
        self.action_select_language.setShortcut('Ctrl+L')
        self.action_select_theme = QtWidgets.QAction(main_window)
        self.action_select_theme.setObjectName("action_select_theme")
        self.action_select_theme.setShortcut('Ctrl+T')

        #************************** HELP **************************"
        self.help_change_range = QtWidgets.QAction(main_window)
        self.help_change_range.setObjectName("help_change_range")
        self.help_new_rule = QtWidgets.QAction(main_window)
        self.help_new_rule.setObjectName("help_new_rule")
        self.help_change_rule = QtWidgets.QAction(main_window)
        self.help_change_rule.setObjectName("help_change_rule")
        self.help_search_rule = QtWidgets.QAction(main_window)
        self.help_search_rule.setObjectName("help_search_rule")
        self.help_search_port = QtWidgets.QAction(main_window)
        self.help_search_port.setObjectName("help_search_port")
        self.action_About = QtWidgets.QAction(main_window)
        self.action_About.setObjectName("action_About")
        self.action_About.triggered.connect(lambda: self.openAbout())

        self.file_menu.addAction(self.action_save_scan)
        self.file_menu.addAction(self.action_save_rules)

        self.edit_menu.addAction(self.action_new_rule)
        self.edit_menu.addAction(self.action_change_range)
        self.edit_menu.addAction(self.action_reload_scan)
        
        self.config_menu.addAction(self.action_select_language)
        self.config_menu.addAction(self.action_select_theme)

        self.help_menu.addAction(self.help_change_range)
        self.help_menu.addAction(self.help_new_rule)
        self.help_menu.addAction(self.help_change_rule)
        self.help_menu.addAction(self.help_search_rule)
        self.help_menu.addAction(self.help_search_port)
        self.help_menu.addSeparator()
        self.help_menu.addAction(self.action_About)

        self.menu_bar.addAction(self.file_menu.menuAction())
        self.menu_bar.addAction(self.edit_menu.menuAction())
        self.menu_bar.addAction(self.config_menu.menuAction())
        self.menu_bar.addAction(self.help_menu.menuAction())

        self.tabWidget.setCurrentIndex(0)
        self.main_layout.addWidget(self.tabWidget)
        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, MainWindow):
        # self.translator = QtCore.QTranslator()
        # self.translator.load("Resources/lan/language_en.qm")
        # QtCore.QCoreApplication.installTranslator(self.translator)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Net Guard"))

        #************************************************************
        #************************* TAB SCAN *************************
        #************************************************************
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Scan), _translate("main_window", "Scan"))

        item = self.scan_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Protocol"))
        item = self.scan_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Local Address"))
        item = self.scan_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Remote Address"))
        item = self.scan_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "State"))
        item = self.scan_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "PID"))
        item = self.scan_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Program"))
            
        self.label_rangeTCP.setText(_translate("MainWindow", "TCP Range:"))
        self.label_rangeUDP.setText(_translate("MainWindow", "UDP Range:"))
        
        self.port_scan_btn.setText(_translate("MainWindow", "Update"))
        self.edit_range_btn.setText(_translate("MainWindow", "Modify"))

        #************************************************************
        #************************* TAB RULES ************************
        #************************************************************
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Rules), _translate("MainWindow", "Rules"))

        self.label_rule.setText(_translate("MainWindow", "Name"))
        self.label_profile.setText(_translate("MainWindow", "Profile"))
        self.label_direction.setText(_translate("MainWindow", "Direction"))
        self.search_rule_btn.setText(_translate("MainWindow", "Search"))
        self.comboBox_rule_profile.addItem(_translate("MainWindow",'Any'))
        self.comboBox_rule_profile.addItem(_translate("MainWindow",'Public'))
        self.comboBox_rule_profile.addItem(_translate("MainWindow",'Private'))
        self.comboBox_rule_profile.addItem(_translate("MainWindow",'Domain'))
        
        item = self.rules_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Rule"))
        item = self.rules_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Enable"))
        item = self.rules_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Profile"))
        item = self.rules_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Action"))
        item = self.rules_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Direction"))
        item = self.rules_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Protocol"))
        
        self.reload_rules_table.setText(_translate("MainWindow", "Update"))
        self.new_rule_btn.setText(_translate("MainWindow", "Add"))

        #************************************************************
        #************************* TAB PORTS ************************
        #************************************************************
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Ports), _translate("MainWindow", "Ports"))

        self.search_port_btn.setText(_translate("MainWindow", "Search"))
        self.label_port.setText(_translate("MainWindow", "Port"))
        self.label_service.setText(_translate("MainWindow", "Service"))
        self.label_protocol.setText(_translate("MainWindow", "Protocol"))
        self.comboBox_protocol.addItem(_translate("MainWindow", "Both"))
        self.comboBox_protocol.addItem(_translate("MainWindow", "TCP"))
        self.comboBox_protocol.addItem(_translate("MainWindow", "UDP"))

        item = self.ports_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Port"))
        item = self.ports_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Service"))
        item = self.ports_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Protocol"))
        item = self.ports_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Description"))
        item = self.ports_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Reference"))

        self.previous_table_btn.setText(_translate("MainWindow", "Back"))
        self.next_table_btn.setText(_translate("MainWindow", "Next"))

        #*************************************************************"
        #************************* MENU BAR **************************"
        #*************************************************************"
        
        self.file_menu.setTitle(_translate("MainWindow", "File"))
        self.edit_menu.setTitle(_translate("MainWindow", "Edit"))
        self.config_menu.setTitle(_translate("MainWindow", "Configuration"))
        self.help_menu.setTitle(_translate("MainWindow", "Help"))

        self.action_save_scan.setText(_translate("MainWindow", "Save scan"))
        self.action_save_rules.setText(_translate("MainWindow", "Save rules"))
        
        self.action_new_rule.setText(_translate("MainWindow", "New rule"))
        self.action_change_range.setText(_translate("MainWindow", "Change ports range"))
        self.action_reload_scan.setText(_translate("MainWindow", "Update scan"))

        self.action_select_language.setText(_translate("MainWindow", "Language"))
        self.action_select_theme.setText(_translate("MainWindow", "Theme"))
        
        self.help_change_range.setText(_translate("MainWindow", "Change ports range"))
        self.help_new_rule.setText(_translate("MainWindow", "Add new rule"))
        self.help_change_rule.setText(_translate("MainWindow", "modify rule"))
        self.help_search_rule.setText(_translate("MainWindow", "Search rule"))
        self.help_search_port.setText(_translate("MainWindow", "Search port"))
        self.action_About.setText(_translate("MainWindow", "About Net Guard"))

    # Method to update the table in the scan tab.
    def updateScanTable(self, mainTable):
        #clear the table and get new values
        mainTable.clearContents()
        mainTable.setRowCount(0)
        getData = self.connection_manager.scan_active_ports()
        #insert new values in table
        mainTable.setRowCount(len(getData))
        for row, row_data in enumerate(getData):
            for col, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                mainTable.setItem(row, col, item)
        #update table
        mainTable.repaint()

        #get Range of ports
        getRange = self.connection_manager.get_ports_range()
        tcpRange = getRange[0].splitlines()[4]
        udpRange = getRange[1].splitlines()[4]

        #set Range on labels
        self.label_valueTCP.setText(tcpRange.split(':')[1])
        self.label_valueUDP.setText(udpRange.split(':')[1])

    # Method to update the table in the rules tab
    def updateRulesTable(self, mainTable):
        # Clear the table and get new values
        mainTable.clearContents()
        mainTable.setRowCount(0)
        rules = self.rules_manager.get_all_rules()
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
        self.newTable = self.ports_manager.get_all_ports(self.minValue, self.maxValue)
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
        self.RangeWindow = PortsRangeWindow()
        self.RangeWindow.setUp_window(self.initRangeWindow)
        self.initRangeWindow.exec_()

    def showSearchRuleTable(self):
        icon = QtWidgets.QMessageBox.Information
        name = self.lineEdit_search_rule.text()
        profile = self.comboBox_rule_profile.currentText()
        direction = self.comboBox_rule_direction.currentText()
        self.InitSearchTable = QtWidgets.QDialog()

        self.searchRule = RulesTableCreator()
        self.searchRule.setup_rules_table(self.InitSearchTable, name, profile, direction)

        if self.lineEdit_search_rule.text() == '':
            code = 'Ingrese el nombre de la regla'
            error = 'Debe ingresar el nombre de la regla para poder realizar una búsqueda'
            self.messages_manager.show_message(code, error, icon)
        elif self.searchRule.new_table.rowCount() == 0:
            code = 'No se encontraron datos coincidentes'
            error = 'La búsqueda no arrojo ningún dato coincidente con los parámetros ingresados'
            self.messages_manager.show_message(code, error, icon)
        else: 
            self.InitSearchTable.exec_()
        self.lineEdit_search_rule.clear()
        self.comboBox_rule_profile.setCurrentText('Any')
        self.comboBox_rule_direction.setCurrentText('Any')


    # Method to show a table with the searched ports
    def showSearchPortsTable(self):
        #icon for the exception
        icon = QtWidgets.QMessageBox.Information
        #get the values
        port = self.spinBox_port.value()
        service = self.lineEdit_search.text()
        protocol = self.comboBox_protocol.currentText()

        #initialize new table with TablePortsCreator
        self.InitSearchTable = QtWidgets.QDialog()
        self.TableApp = TablePortsCreator(port, protocol, service)
        self.TableApp.setup_table(self.InitSearchTable)

        #exceptions of the search
        if port >= 49152:
            #port value is´nt registered 
            code = 'Puerto no registrado'
            error = 'El puerto que intenta buscar no se encuentra registrado por la IANA'
            self.messages_manager.show_message(code, error, icon)
        elif service == '' and port == 0:
            #empty values of search
            code = 'No se puede realizar la búsqueda'
            error = 'La búsqueda no se puede procesar como la especifico, revise la ayuda para realizar búsquedas'
            self.messages_manager.show_message(code, error, icon)
        elif self.TableApp.new_table.rowCount() == 0:
            #data is´nt on the DB
            code = 'No se encontraron datos coincidentes'
            error = 'La búsqueda no arrojó ningún dato coincidente con los parámetros ingresados'
            self.messages_manager.show_message(code, error, icon)
        else:
            #show the results
            self.InitSearchTable.exec_()
        self.lineEdit_search.clear()
        self.spinBox_port.setValue(0)
        self.comboBox_protocol.setCurrentIndex(0)
    
    #Method to show a windows with more information
    def showScanTableInfo(self):
        code = 'Función en construcción'
        message = 'Función showScanTableInfo en construcción'
        icon = QtWidgets.QMessageBox.Information
        self.messages_manager.show_message(code, message, icon)

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
        self.messages_manager.show_message(code, message, icon)

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
        ui_about = UiDialog()
        ui_about.setupUi(about_dialog)
        about_dialog.exec_()