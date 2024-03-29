# ***************************************************
# FILE: MainWindow.py
#
# -*- coding: utf-8 -*-
#
# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
#
# DESCRIPTION:
# The Ui_MainWindow class is a key component of the Net Guard desktop application.
# It serves as the user interface definition for the main application window.
# This class is responsible for defining the layout and behavior of the
# application's graphical user interface (GUI).
#
# AUTHOR: Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

from PyQt5 import QtCore, QtGui, QtWidgets
from Controller.Configuration import LanguageManager, ThemeManager, ErrorDataManager
from Controller.Ports import GetPortsData, TableCounter, ErrorPorts
from Controller.Rules import FirewallManager, FirewallManagerError
from Controller.Report import ReportPDF, ErrorReport
from Controller.Scan import ScanPorts, ScanError
from .RulesTab import RulesTableCreator
from .PortsTab import TablePortsCreator
from .ScanTab import PortsRangeWindow
from .Alerts import PopUpMessage
from .About import UiDialog
from .SetText import SetCurrentText
from .Styles import SetCurrentTheme


class Ui_MainWindow(object):
    '''
    A class for configuring and setting up the user interface of the main window.

    Attributes:
        report_manager (ReportPDF): An object for managing PDF reports.
        central_widget (QtWidgets.QWidget): The central widget of the main window.
        main_layout (QtWidgets.QVBoxLayout): The main layout of the central widget.
        tabWidget (QtWidgets.QTabWidget): A tab widget for managing different tabs.

    Methods:
        setupUi(self, main_window)
            Sets up the user interface components of the main window.

        retranslateUi(self, MainWindow)
            Translates and sets text labels for user interface elements.

        update_scan_table(self, mainTable)
            Updates the table in the "Scan" tab with scan data.

        update_rules_table(self, mainTable)
            Updates the table in the "Rules" tab with rule data.

        update_ports_table(self, mainTable)
            Updates the table in the "Ports" tab with port data.

        sort_table(self, table, column)
            Sorts a table based on the specified column.

        show_range_ports_window(self)
            Opens a dialog to change port range settings.

        show_search_rule_table(self)
            Displays a table with search results based on rule criteria.

        show_search_ports_table(self)
            Displays a table with search results based on port criteria.

        show_scan_table_info(self)
            Displays information about the scan table (development status).

        show_new_rule_window(self):
            Opens a dialog to create a new rule.

        show_ports_table_info(self)
            Displays information about the ports table (development status).

        next_value(self, mainTable)
            Displays the next set of values in the Ports tab table.

        previous_value(self, mainTable)
            Displays the previous set of values in the Ports tab table.

        show_window_about(self)
            Opens a dialog displaying information about the application.

    '''
    def __init__(self) -> None:
        self.counter = TableCounter(1, 65535)
        self.current_text = SetCurrentText()
        self.theme = SetCurrentTheme()
        self.messages_manager = PopUpMessage(self.current_text, self.theme)
        self.icon_information = QtWidgets.QMessageBox.Information
        self.icon_critical = QtWidgets.QMessageBox.Critical

    def setupUi(self, main_window: QtWidgets.QMainWindow):
        '''
        Sets up the user interface components of the main window.

        Args:
            main_window (QtWidgets.QMainWindow): The main application window.

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.setupUi(main_window)

        '''
        main_window.setObjectName("main_window")
        main_window.resize(755, 616)
        main_window.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        self.change_theme(main_window)

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.tabWidget = QtWidgets.QTabWidget(self.central_widget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setObjectName("tabWidget")

        # ************************************************************
        # ************************* TAB SCAN *************************
        # ************************************************************
        self.tab_Scan = QtWidgets.QWidget()
        self.tab_Scan.setObjectName("tab_Scan")
        self.tabWidget.addTab(self.tab_Scan, "")
        self.connection_manager = ScanPorts()

        # ************************** Table ***************************"
        self.scan_table = QtWidgets.QTableWidget(self.tab_Scan)
        self.scan_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.scan_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.scan_table.setObjectName("scan_table")
        self.scan_table.setColumnCount(6)
        self.scan_table.cellDoubleClicked.connect(self.show_scan_table_info)
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

        # ************************** Footer **************************"
        self.label_rangeTCP = QtWidgets.QLabel(self.tab_Scan)
        self.label_rangeTCP.setObjectName("label_rangeTCP")
        self.label_valueTCP = QtWidgets.QLabel(self.tab_Scan)
        self.label_valueTCP.setObjectName("label_valueTCP")

        self.label_rangeUDP = QtWidgets.QLabel(self.tab_Scan)
        self.label_rangeUDP.setObjectName("label_rangeUDP")
        self.label_valueUDP = QtWidgets.QLabel(self.tab_Scan)
        self.label_valueUDP.setObjectName("label_valueUDP")

        self.update_scan_table(self.scan_table)

        self.port_scan_btn = QtWidgets.QToolButton(self.tab_Scan)
        self.port_scan_btn.setFixedSize(101, 26)
        self.port_scan_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.port_scan_btn.setObjectName("port_scan_btn")
        self.port_scan_btn.clicked.connect(lambda: self.update_scan_table(self.scan_table))

        self.edit_range_btn = QtWidgets.QToolButton(self.tab_Scan)
        self.edit_range_btn.setFixedSize(101, 26)
        self.edit_range_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_range_btn.setObjectName("edit_range_btn")
        self.edit_range_btn.clicked.connect(lambda: self.show_range_ports_window())
        self.edit_range_btn.clicked.connect(lambda: self.update_scan_table(self.scan_table))

        self.scan_table_layout = QtWidgets.QGridLayout(self.tab_Scan)
        self.scan_table_layout.addWidget(self.scan_table, 0, 0, 1, 3)
        self.scan_table_layout.addWidget(self.label_rangeTCP, 1, 0)
        self.scan_table_layout.addWidget(self.label_valueTCP, 1, 1)
        self.scan_table_layout.addWidget(self.label_rangeUDP, 2, 0)
        self.scan_table_layout.addWidget(self.label_valueUDP, 2, 1)
        self.scan_table_layout.addWidget(self.port_scan_btn, 3, 0)
        self.scan_table_layout.addWidget(self.edit_range_btn, 3, 1)

        # *************************************************************"
        # ************************* TAB RULES *************************"
        # *************************************************************"
        self.tab_Rules = QtWidgets.QWidget()
        self.get_searched_rules = RulesTableCreator(self.current_text, self.theme)
        self.tab_Rules.setObjectName("tab_Rules")
        self.tabWidget.addTab(self.tab_Rules, "")

        # ************************** Header ***************************"
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

        self.search_rule_btn.setFixedSize(101, 26)
        self.search_rule_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_rule_btn.setObjectName("search_rule_btn")
        self.search_rule_btn.clicked.connect(self.show_search_rule_table)

        # ************************** Table ***************************"
        self.rules_table = QtWidgets.QTableWidget(self.tab_Rules)
        self.rules_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.rules_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.rules_table.setObjectName("rules_table")
        self.rules_table.setColumnCount(6)
        self.rules_table.cellDoubleClicked.connect(lambda row: self.get_searched_rules.get_selected_rule(self.rules_table, row))
        self.rules_table.cellDoubleClicked.connect(lambda: self.update_rules_table(self.rules_table))
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

        self.update_rules_table(self.rules_table)

        # ************************** Buttons ***************************"
        self.reload_rules_table = QtWidgets.QToolButton(self.tab_Rules)
        self.reload_rules_table.setFixedSize(101, 26)
        self.reload_rules_table.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reload_rules_table.setObjectName("reload_rules_table")
        self.reload_rules_table.clicked.connect(lambda: self.update_rules_table(self.rules_table))

        self.new_rule_btn = QtWidgets.QToolButton(self.tab_Rules)
        self.new_rule_btn.setFixedSize(101, 26)
        self.new_rule_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.new_rule_btn.setObjectName("new_rule_btn")
        self.new_rule_btn.clicked.connect(lambda: self.show_new_rule_window())
        self.new_rule_btn.clicked.connect(lambda: self.update_rules_table(self.rules_table))

        self.rules_table_layout = QtWidgets.QGridLayout(self.tab_Rules)
        self.rules_table_layout.addWidget(self.label_rule, 0, 0)
        self.rules_table_layout.addWidget(self.lineEdit_search_rule, 0, 1)
        self.rules_table_layout.addWidget(self.label_profile, 0, 2)
        self.rules_table_layout.addWidget(self.comboBox_rule_profile, 0, 3)
        self.rules_table_layout.addWidget(self.label_direction, 0, 4)
        self.rules_table_layout.addWidget(self.comboBox_rule_direction, 0, 5)
        self.rules_table_layout.addWidget(self.search_rule_btn, 0, 6)
        self.rules_table_layout.addWidget(self.rules_table, 1, 0, 1, 7)
        self.rules_table_layout.addWidget(self.reload_rules_table, 2, 0)
        self.rules_table_layout.addWidget(self.new_rule_btn, 2, 1)

        # *************************************************************"
        # ************************* TAB PORTS *************************"
        # *************************************************************"
        self.tab_Ports = QtWidgets.QWidget()
        self.tab_Ports.setObjectName("tab_Ports")
        self.tabWidget.addTab(self.tab_Ports, "")

        # ************************** HEADER ***************************"
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
        self.search_port_btn.clicked.connect(self.show_search_ports_table)

        # *************************** TABLE ***************************"
        self.ports_table = QtWidgets.QTableWidget(self.tab_Ports)
        self.ports_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ports_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ports_table.setObjectName("ports_table")
        self.ports_table.setColumnCount(5)
        self.ports_table.setRowCount(14)
        self.ports_table.cellDoubleClicked.connect(self.show_ports_table_info)



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

        self.update_ports_table(self.ports_table)

        # ************************** BUTTONS **************************"
        self.previous_table_btn = QtWidgets.QToolButton(self.tab_Ports)
        self.previous_table_btn.setFixedSize(101, 26)
        self.previous_table_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.previous_table_btn.setObjectName("previous_table_btn")
        self.previous_table_btn.clicked.connect(lambda: self.previous_value(self.ports_table))

        self.next_table_btn = QtWidgets.QToolButton(self.tab_Ports)
        self.next_table_btn.setFixedSize(101, 26)
        self.next_table_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next_table_btn.setObjectName("next_table_btn")
        self.next_table_btn.clicked.connect(lambda: self.next_value(self.ports_table))

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

        # *************************************************************"
        # ************************* MENU BAR **************************"
        # *************************************************************"
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

        # ************************** FILE **************************"
        self.action_save_scan = QtWidgets.QAction(main_window)
        self.action_save_scan.setShortcut('Ctrl+S')
        self.action_save_scan.setObjectName("action_save_scan")
        self.action_save_scan.triggered.connect(lambda: self.save_report(self.scan_table, True))
        self.action_save_rules = QtWidgets.QAction(main_window)
        self.action_save_rules.setShortcut('Ctrl+R')
        self.action_save_rules.setObjectName("action_save_rules")
        self.action_save_rules.triggered.connect(lambda: self.save_report(self.rules_table, False))

        # ************************** EDIT **************************"
        self.action_new_rule = QtWidgets.QAction(main_window)
        self.action_new_rule.setShortcut('Ctrl+N')
        self.action_new_rule.setObjectName("action_new_rule")
        self.action_new_rule.triggered.connect(lambda: self.show_new_rule_window())
        self.action_new_rule.triggered.connect(lambda: self.update_rules_table(self.rules_table))
        self.action_change_range = QtWidgets.QAction(main_window)
        self.action_change_range.setShortcut('Ctrl+C')
        self.action_change_range.setObjectName("action_change_range")
        self.action_change_range.triggered.connect(lambda: self.show_range_ports_window())
        self.action_change_range.triggered.connect(lambda: self.update_scan_table(self.scan_table))
        self.action_reload_scan = QtWidgets.QAction(main_window)
        self.action_reload_scan.setShortcut('Ctrl+E')
        self.action_reload_scan.setObjectName("action_reload_scan")
        self.action_reload_scan.triggered.connect(lambda: self.update_scan_table(self.scan_table))

        # ************************** CONFIG **************************"
        self.menu_select_language = QtWidgets.QMenu(self.menu_bar)
        self.menu_select_language.setObjectName("menu_select_language")
        self.action_select_Spanish = QtWidgets.QAction(self.menu_select_language)
        self.action_select_Spanish.setObjectName("action_select_Spanish")
        self.action_select_Spanish.triggered.connect(lambda: self.set_language('es'))
        self.action_select_Spanish.triggered.connect(lambda: self.current_text.set_main_window(self, main_window))
        self.action_select_english = QtWidgets.QAction(self.menu_select_language)
        self.action_select_english.setObjectName("action_select_english")
        self.action_select_english.triggered.connect(lambda: self.set_language('en'))
        self.action_select_english.triggered.connect(lambda: self.current_text.set_main_window(self, main_window))

        self.menu_select_theme = QtWidgets.QMenu(self.menu_bar)
        self.menu_select_theme.setObjectName("menu_select_theme")
        self.action_select_dark = QtWidgets.QAction(self.menu_select_theme)
        self.action_select_dark.setObjectName("action_select_dark")
        self.action_select_dark.triggered.connect(lambda: self.set_theme('dark'))
        self.action_select_dark.triggered.connect(lambda: self.change_theme(main_window))
        self.action_select_light = QtWidgets.QAction(self.menu_select_theme)
        self.action_select_light.setObjectName("action_select_light")
        self.action_select_light.triggered.connect(lambda: self.set_theme('light'))
        self.action_select_light.triggered.connect(lambda: self.change_theme(main_window))

        # ************************** HELP **************************"
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
        self.action_About.triggered.connect(lambda: self.show_window_about())

        # ************************** ACTIONS **************************"
        self.file_menu.addAction(self.action_save_scan)
        self.file_menu.addAction(self.action_save_rules)

        self.edit_menu.addAction(self.action_new_rule)
        self.edit_menu.addAction(self.action_change_range)
        self.edit_menu.addAction(self.action_reload_scan)

        self.config_menu.addMenu(self.menu_select_language)
        self.menu_select_language.addAction(self.action_select_Spanish)
        self.menu_select_language.addAction(self.action_select_english)
        self.config_menu.addMenu(self.menu_select_theme)
        self.menu_select_theme.addAction(self.action_select_dark)
        self.menu_select_theme.addAction(self.action_select_light)

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

        self.rule_name_missing_message = ''
        self.rule_name_missing_description = ''

        self.no_matching_data_message = ''
        self.no_matching_data_description = ''

        self.unregistered_port_message = ''
        self.unregistered_port_description = ''

        self.invalid_search_message = ''
        self.invalid_search_description = ''

        self.port_not_found_message = ''
        self.port_not_found_description = ''

        self.report_saved_message = ''

        self.current_text.set_main_window(self, main_window)
        
    def update_scan_table(self, mainTable: QtWidgets.QTableWidget):
        '''
        Updates the table in the "Scan" tab with scan data.

        Args:
            mainTable (QtWidgets.QTableWidget): The table widget in the "Scan" tab.

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.update_scan_table(mainTable)

        '''
        try:
            mainTable.clearContents()
            mainTable.setRowCount(0)
            getData = self.connection_manager.scan_active_ports()
            mainTable.setRowCount(len(getData))
            for row, row_data in enumerate(getData):
                for col, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    mainTable.setItem(row, col, item)
            mainTable.repaint()

            getRange = self.connection_manager.get_ports_range()
            if getRange:
                tcpRange = getRange[0].splitlines()[4]
                udpRange = getRange[1].splitlines()[4]
                self.label_valueTCP.setText(tcpRange.split(':')[1])
                self.label_valueUDP.setText(udpRange.split(':')[1])
            else:
                self.messages_manager.show_message('Unable to get range', '', self.icon_critical)
        except ScanError as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_Update_Scan_Table', str(exception), self.icon_information)


    def update_rules_table(self, mainTable: QtWidgets.QTableWidget):
        '''
        Updates the table in the "Rules" tab with rule data.

        Args:
            mainTable (QtWidgets.QTableWidget): The table widget in the "Rules" tab.

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.update_rules_table(mainTable)

        '''
        self.rules_manager = FirewallManager()
        mainTable.clearContents()
        mainTable.setRowCount(0)
        try:
            rules = self.rules_manager.get_all_rules()
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
            mainTable.repaint()
        except FirewallManagerError as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_Update_Rules_Table', str(exception), self.icon_information)

    def update_ports_table(self, mainTable: QtWidgets.QTableWidget):
        '''
        Updates the table in the "Ports" tab with port data.

        Args:
            mainTable (QtWidgets.QTableWidget): The table widget in the "Ports" tab.

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.update_ports_table(mainTable)

        '''
        self.ports_manager = GetPortsData()
        self.minValue = self.counter.current_value
        self.maxValue = self.counter.current_value + 13
        try:
            self.newTable = self.ports_manager.get_all_ports(self.minValue, self.maxValue)
            if self.newTable:
                mainTable.clearContents()
                for row, row_data in enumerate(self.newTable):
                    for col, col_data in enumerate(row_data):
                        item = QtWidgets.QTableWidgetItem(str(col_data))
                        mainTable.setItem(row, col, item)
                mainTable.repaint()
        except ErrorPorts as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_Update_Ports_Table', str(exception), self.icon_information)

    def sort_table(self, table: QtWidgets.QTableWidget, column: int):
        '''
        sorts the selected table by the selected column.

        Args:
            table (QtWidgets.QTableWidget). The table widget in the selected tab.
            column (int). The selected column of the table.

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.sort_table(table, 2)

        '''
        table.sortItems(column, QtCore.Qt.AscendingOrder)

    def show_range_ports_window(self):
        '''
        Initializes and displays a dialog to change port range settings.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.show_range_ports_window()

        '''
        self.initRangeWindow = QtWidgets.QDialog()
        self.RangeWindow = PortsRangeWindow(self.current_text, self.theme)
        self.RangeWindow.setUp_window(self.initRangeWindow)
        self.initRangeWindow.exec_()

    def show_search_rule_table(self):
        '''
        Displays a table with search results based on rule criteria.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.show_search_rule_table()

        '''
        name = self.lineEdit_search_rule.text()
        profile = self.comboBox_rule_profile.currentIndex()
        direction = self.comboBox_rule_direction.currentIndex()
        self.InitSearchTable = QtWidgets.QDialog()
        self.searchRule = RulesTableCreator(self.current_text, self.theme)
        try:
            self.searchRule.setup_rules_table(self.InitSearchTable, name, profile, direction)

            if self.lineEdit_search_rule.text() == '':
                self.messages_manager.show_message(self.rule_name_missing_message, self.rule_name_missing_description, self.icon_information)
            elif self.searchRule.new_table.rowCount() == 0:
                self.messages_manager.show_message(self.no_matching_data_message, self.no_matching_data_description, self.icon_information)
            else:
                self.InitSearchTable.exec_()
            self.lineEdit_search_rule.clear()
            self.comboBox_rule_profile.setCurrentIndex(0)
            self.comboBox_rule_direction.setCurrentIndex(0)
        except FirewallManagerError as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_Search_Rule', str(exception), self.icon_information)


    def show_search_ports_table(self):
        '''
        Displays a table with search results based on port criteria.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.show_search_ports_table()

        '''
        try:
            port = self.spinBox_port.value()
            service = self.lineEdit_search.text()
            protocol = self.comboBox_protocol.currentIndex()

            if service == '' and port == 0:
                self.messages_manager.show_message(self.invalid_search_message, self.invalid_search_description, self.icon_information)
            elif port >= 49152:
                self.messages_manager.show_message(self.unregistered_port_message, self.unregistered_port_description, self.icon_information)
            else:
                self.InitSearchTable = QtWidgets.QDialog()
                self.TableApp = TablePortsCreator(port, protocol, service, self.current_text, self.theme)
                self.TableApp.setup_table(self.InitSearchTable)
                if self.TableApp.new_table.rowCount() == 0:
                    self.messages_manager.show_message(self.port_not_found_message, self.port_not_found_description, self.icon_information)
                else:
                    self.InitSearchTable.exec_()
            self.lineEdit_search.clear()
            self.spinBox_port.setValue(0)
            self.comboBox_protocol.setCurrentIndex(0)
        except ErrorPorts as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_Search_Port', str(exception), self.icon_information)


    def show_scan_table_info(self):
        '''
        Displays a dialog with information about the scan table (development status).

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.show_scan_table_info()

        '''
        code = 'This does not work'
        message = 'still in develop'
        self.messages_manager.show_message(code, message, self.icon_information)

    def show_new_rule_window(self):
        '''
        Opens a dialog to create a new rule.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.show_new_rule_window()

        '''
        try:
            self.init_rules_dialog = QtWidgets.QDialog()
            self.RuleWindow = RulesTableCreator(self.current_text, self.theme)
            self.RuleWindow.init_rule_window(self.init_rules_dialog)
            self.init_rules_dialog.exec_()
        except FirewallManagerError as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_New_Rule', exception, self.icon_critical)

    def show_ports_table_info(self):
        '''
        Displays a dialog with information about the ports table (development status).

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.show_ports_table_info()

        '''
        code = 'This does not work'
        message = 'still in develop'
        
        self.messages_manager.show_message(code, message, self.icon_information)

    def save_report(self, table: QtWidgets.QTableWidget, value: bool):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        QtWidgets.QApplication.processEvents()

        self.report_manager = ReportPDF()
        report_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
        try:
            self.report_manager.save_to_PDF(report_path, table, value)
            QtWidgets.QApplication.restoreOverrideCursor()
            self.messages_manager.show_message(self.report_saved_message, '', self.icon_information)
        except ErrorReport as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_Save_Report', str(exception), self.icon_information)

    def set_language(self, language: str):
        self.language = LanguageManager()
        try:
            self.language.set_language(language)
        except ErrorDataManager as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_Set_Language', str(exception), self.icon_information)

    def set_theme(self, theme: str):
        self.themeManager = ThemeManager()
        try:
            self.themeManager.set_theme(theme)
        except ErrorDataManager as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_Set_Theme', str(exception), self.icon_information)

    def change_theme(self, main_window):
        try:
            self.theme.set_selected_theme(main_window)
        except ErrorDataManager as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.messages_manager.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.messages_manager.show_message('ERROR: MainWindow_Change_Theme', str(exception), self.icon_information)

    def next_value(self, mainTable: QtWidgets.QTableWidget):
        '''
        Displays the next 14 values on the table in the "Ports" tab.

        Args:
            mainTable (QtWidgets.QTableWidget): The table widget in the "Ports" tab.

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.next_value(mainTable)

        '''
        self.counter.next()
        self.update_ports_table(mainTable)

    def previous_value(self, mainTable: QtWidgets.QTableWidget):
        '''
        Displays the previous 14 values on the table in the "Ports" tab.

        Args:
            mainTable (QtWidgets.QTableWidget): The table widget in the "Ports" tab.

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.previous_value(mainTable)

        '''
        self.counter.previous()
        self.update_ports_table(mainTable)

    def show_window_about(self):
        '''
        Opens a dialog displaying information about the application.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            ui = Ui_MainWindow()
            ui.show_window_about()

        '''
        about_dialog = QtWidgets.QDialog()
        ui_about = UiDialog()
        ui_about.setupUi(about_dialog, self.current_text, self.theme)
        about_dialog.exec_()
