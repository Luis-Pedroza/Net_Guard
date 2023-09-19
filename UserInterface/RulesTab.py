# ***************************************************
# FILE: UI_Rules_Tab.py
#
# DESCRIPTION:
#
# The RulesTableCreator class is used for creating and setting up a table to
# display firewall rules information, as well as for managing the
# addition, editing, and deletion of firewall rules.
#
# AUTHOR:  Luis Pedroza
# CREATED: 17/04/2023 (dd/mm/yy)
# ***************************************************

from PyQt5 import QtCore, QtWidgets, QtGui
from Controller.Rules import FirewallManager, FirewallManagerError
from .Alerts import PopUpMessage
from .SetText import SetCurrentText


class RulesTableCreator(object):
    '''
    A class for creating and setting up a table to display firewall rules information.

    Attributes:
        message (PopUpMessage): A class for displaying messages.
        rules_connection (FirewallManager): An object for managing firewall rules.
        icon (QtWidgets.QMessageBox.Icon): An icon for message boxes.

    Methods:
        __init__(self)
            Initialize the RulesTableCreator class.

        setup_rules_table(self, main_window, name, profile, direction)
            Set up the table to display firewall rules information based on search criteria.

        init_rule_window(self, Form, action=False, rule=None)
            Initialize a window for adding, editing, or deleting firewall rules.

        enable_selected(self, text, line_edit_widget)
            Enable or disable input fields based on selected options.

        add_new_rule(self)
            Add a new firewall rule.

        get_selected_rule(self, table, row)
            Show detailed information for a selected firewall rule.

        setUp_filled_window(self, form, rule)
            Set up the window with filled information for editing a rule.

        edit_selected_rule(self, rule)
            Edit a selected firewall rule.

        delete_selected_rule(self, rule)
            Delete a selected firewall rule.

    '''
    def __init__(self):
        self.current_text = SetCurrentText()
        self.message = PopUpMessage()
        self.rules_connection = FirewallManager()
        self.icon = QtWidgets.QMessageBox.Information
        self.icon_critical = QtWidgets.QMessageBox.Critical

    def setup_rules_table(self, main_window: QtWidgets.QMainWindow, name: str, profile: int, direction: int):
        '''
        Set up the table to display firewall rules information based on search criteria.

        Args:
            main_window (QtWidgets.QMainWindow): The main window to display the table.
            name (str): The name of the rule to search for.
            profile (str): The profile of the rule to search for.
            direction (str): The direction of the rule to search for.

        Returns:
            None

        Raises:
            None

        Example Usage:
            table_creator = RulesTableCreator()
            table_creator.setup_rules_table(main_window, "MyRule", "Domain", "Inbound")

        '''
        profile = 7 if profile == 0 else profile

        main_window.setObjectName("main_window")
        main_window.setFixedSize(760, 350)
        main_window.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        try:
            rules_data_list = self.rules_connection.get_searched_rule(name, profile, direction)

            if rules_data_list:
                self.Form = QtWidgets.QWidget()
                self.new_table = QtWidgets.QTableWidget(main_window)
                self.new_table.setColumnCount(6)
                self.new_table.setRowCount(len(rules_data_list))
                self.new_table.setGeometry(QtCore.QRect(1, 0, 759, 511))
                self.new_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.new_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
                self.new_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                self.new_table.cellDoubleClicked.connect(lambda row: self.get_selected_rule(self.new_table, row))

                item = QtWidgets.QTableWidgetItem()
                self.new_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                item = QtWidgets.QTableWidgetItem()
                self.new_table.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                self.new_table.setHorizontalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                self.new_table.setHorizontalHeaderItem(2, item)
                item = QtWidgets.QTableWidgetItem()
                self.new_table.setHorizontalHeaderItem(3, item)
                item = QtWidgets.QTableWidgetItem()
                self.new_table.setHorizontalHeaderItem(4, item)
                item = QtWidgets.QTableWidgetItem()
                self.new_table.setHorizontalHeaderItem(5, item)

                for i, row in enumerate(rules_data_list):
                    item = QtWidgets.QTableWidgetItem(str(row[0]))
                    self.new_table.setItem(i, 0, item)
                    item = QtWidgets.QTableWidgetItem(str(row[1]))
                    self.new_table.setItem(i, 1, item)
                    item = QtWidgets.QTableWidgetItem(str(row[2]))
                    self.new_table.setItem(i, 2, item)
                    item = QtWidgets.QTableWidgetItem(str(row[3]))
                    self.new_table.setItem(i, 3, item)
                    item = QtWidgets.QTableWidgetItem(str(row[4]))
                    self.new_table.setItem(i, 4, item)
                    item = QtWidgets.QTableWidgetItem(str(row[5]))
                    self.new_table.setItem(i, 5, item)
                self.current_text.set_rules_table(self, main_window)

            else: self.new_table = QtWidgets.QTableWidget(main_window)

        except FirewallManagerError as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.message.show_message(error_code, str(error_description), self.icon_critical)
        except Exception as exception:
            self.message.show_message('ERROR_RulesTableCreator_SetUp_Rules', str(exception), self.icon)


    def init_rule_window(self, Form: QtWidgets.QDialog, action: bool = False, rule: list = None):
        '''
        Initialize a window for adding, editing, or deleting firewall rules.

        Args:
            Form (QtWidgets.QDialog): The form/window to initialize.
            action (bool, optional): Flag indicating whether the window is for editing (True)
                or Creating (False) a rule. Default is False.
            rule (list, optional): The rule data to populate the window for editing. Default is None.

        Returns:
            None

        Raises:
            None

        Example Usage:
            table_creator = RulesTableCreator()
            table_creator.init_rule_window(new_form, True, search)

        '''
        Form.setObjectName("Form")
        Form.setFixedSize(400, 500)
        Form.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))

        self.label_name = QtWidgets.QLabel(Form)
        self.label_name.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.label_name.setObjectName("label_name")
        self.line_edit_name = QtWidgets.QLineEdit(Form)
        self.line_edit_name.setGeometry(QtCore.QRect(70, 20, 291, 20))
        self.line_edit_name.setObjectName("line_edit_name")

        self.label_description = QtWidgets.QLabel(Form)
        self.label_description.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.label_description.setObjectName("label_description")
        self.text_edit_description = QtWidgets.QTextEdit(Form)
        self.text_edit_description.setGeometry(QtCore.QRect(20, 70, 340, 70))
        self.text_edit_description.setObjectName("text_edit_description")

        self.checkBox_enable = QtWidgets.QCheckBox(Form)
        self.checkBox_enable.setGeometry(QtCore.QRect(30, 160, 70, 17))
        self.checkBox_enable.setObjectName("checkBox_enable")

        self.label_direction = QtWidgets.QLabel(Form)
        self.label_direction.setGeometry(QtCore.QRect(30, 200, 61, 16))
        self.label_direction.setObjectName("label_direction")
        self.comboBox_direction = QtWidgets.QComboBox(Form)
        self.comboBox_direction.setGeometry(QtCore.QRect(80, 200, 110, 22))
        self.comboBox_direction.setObjectName("comboBox_direction")

        self.label_action = QtWidgets.QLabel(Form)
        self.label_action.setGeometry(QtCore.QRect(30, 244, 47, 13))
        self.label_action.setObjectName("labelActionPort")
        self.comboBox_action = QtWidgets.QComboBox(Form)
        self.comboBox_action.setGeometry(QtCore.QRect(80, 240, 110, 22))
        self.comboBox_action.setObjectName("comboBoxActionPort")

        self.label_protocol = QtWidgets.QLabel(Form)
        self.label_protocol.setGeometry(QtCore.QRect(30, 284, 51, 16))
        self.label_protocol.setObjectName("label_protocol")
        self.comboBox_protocol = QtWidgets.QComboBox(Form)
        self.comboBox_protocol.setGeometry(QtCore.QRect(80, 280, 110, 22))
        self.comboBox_protocol.setObjectName("comboBox_protocol")

        self.label_profile = QtWidgets.QLabel(Form)
        self.label_profile.setGeometry(QtCore.QRect(30, 324, 51, 16))
        self.label_profile.setObjectName("label_profile")
        self.comboBox_profile = QtWidgets.QComboBox(Form)
        self.comboBox_profile.setGeometry(QtCore.QRect(80, 320, 110, 22))
        self.comboBox_profile.setObjectName("comboBox_profile")

        self.label_port = QtWidgets.QLabel(Form)
        self.label_port.setGeometry(QtCore.QRect(210, 204, 47, 13))
        self.label_port.setObjectName("label_port")
        self.comboBox_port = QtWidgets.QComboBox(Form)
        self.comboBox_port.setGeometry(QtCore.QRect(260, 200, 100, 22))
        self.comboBox_port.setObjectName("comboBoxPort")
        self.line_edit_port = QtWidgets.QLineEdit(Form)
        self.line_edit_port.setGeometry(QtCore.QRect(210, 240, 150, 22))
        self.line_edit_port.setObjectName("lineEditPort")
        self.comboBox_port.currentIndexChanged.connect(lambda text: self.enable_selected(text, self.line_edit_port))
        self.enable_selected(self.comboBox_port.currentIndex(), self.line_edit_port)

        self.label_program = QtWidgets.QLabel(Form)
        self.label_program.setGeometry(QtCore.QRect(210, 280, 51, 16))
        self.label_program.setObjectName("label_program")
        self.comboBox_program = QtWidgets.QComboBox(Form)
        self.comboBox_program.setGeometry(QtCore.QRect(280, 280, 80, 22))
        self.comboBox_program.setObjectName("comboBox_program")
        self.line_edit_program = QtWidgets.QLineEdit(Form)
        self.line_edit_program.setGeometry(QtCore.QRect(210, 320, 151, 20))
        self.line_edit_program.setObjectName("lineEditProgram")
        self.comboBox_program.currentIndexChanged.connect(lambda text: self.enable_selected(text, self.line_edit_program))
        self.enable_selected(self.comboBox_program.currentIndex(), self.line_edit_program)

        self.label_IP = QtWidgets.QLabel(Form)
        self.label_IP.setGeometry(QtCore.QRect(30, 350, 100, 20))
        self.label_IP.setObjectName("label_IP")
        self.text_edit_IP = QtWidgets.QTextEdit(Form)
        self.text_edit_IP.setGeometry(QtCore.QRect(30, 370, 340, 70))
        self.text_edit_IP.setObjectName("text_edit_IP")

        self.btn_left = QtWidgets.QPushButton(Form)
        self.btn_left.setGeometry(QtCore.QRect(70, 450, 101, 26))
        self.btn_left.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_left.setObjectName("btn_left")

        self.btn_right = QtWidgets.QPushButton(Form)
        self.btn_right.setGeometry(QtCore.QRect(250, 450, 101, 26))
        self.btn_right.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_right.setObjectName("btn_right")

        self.txt_add_btn = ''
        self.txt_cancel_btn = ''

        self.txt_edit_btn = ''
        self.txt_delete_btn = ''

        self.name_missing_error = ''
        self.name_missing_description = ''

        self.rule_unable = ''

        self.deleted_alert = ''
        self.rule_changed = ''
        self.added_rule = ''


        self.current_text.set_rules_window(self, Form)

        if action:
            self.setUp_filled_window(Form, rule)
        else:
            self.btn_left.setText(self.txt_add_btn)
            self.btn_left.clicked.connect(self.add_new_rule)
            self.btn_left.clicked.connect(Form.close)
            self.btn_right.setText(self.txt_cancel_btn)
            self.btn_right.clicked.connect(Form.close)

    def enable_selected(self, selection: int, line_edit_widget: QtWidgets.QLineEdit):
        '''
        Enable or disable input fields based on selected options.

        Args:
            text (str): The selected option.
            line_edit_widget (QtWidgets.QLineEdit or QtWidgets.QTextEdit): The input widget to enable or disable.

        Returns:
            None

        Raises:
            None

        Example Usage:
            table_creator = RulesTableCreator()
            table_creator.enable_selected("Any", line_edit_widget)

        '''
        if selection == 0:
            line_edit_widget.setEnabled(False)
        else:
            line_edit_widget.setEnabled(True)

    def add_new_rule(self):
        '''
        Add a new firewall rule.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            table_creator = RulesTableCreator()
            table_creator.add_new_rule()

        '''
        try:
            rule_data = {
                "name": self.line_edit_name.text(),
                "description": self.text_edit_description.toPlainText(),
                "enable": self.checkBox_enable.isChecked(),
                "direction": self.comboBox_direction.currentIndex(),
                "action": self.comboBox_action.currentIndex(),
                "protocol": self.comboBox_protocol.currentText(),
                "profile": self.comboBox_profile.currentIndex(),
                "port": None if self.comboBox_port.currentIndex() == 0 else self.line_edit_port.text(),
                "selected_port": self.line_edit_port.text(),
                "program": None if self.comboBox_program.currentIndex() == 0 else self.line_edit_program.text(),
                "selected_program": self.line_edit_program.text(),
                "ip": None if self.text_edit_IP.toPlainText() == '' else self.text_edit_IP.toPlainText()
            }
            if rule_data["name"] != '':
                self.rules_connection.add_new_rule(rule_data)
                self.message.show_message(self.added_rule, '', self.icon)
            else:
                self.message.show_message(self.name_missing_error, self.name_missing_description, self.icon)
        except FirewallManagerError as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.message.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.message.show_message('ERROR_RulesTableCreator_Add', str(exception), self.icon)


    def get_selected_rule(self, table: QtWidgets.QTableWidget, row: int):
        '''
        Show detailed information for a selected firewall rule.

        Args:
            table (QtWidgets.QTableWidget): The table containing firewall rules.
            row (int): The selected row.

        Returns:
            None

        Raises:
            None

        Example Usage:
            table_creator = RulesTableCreator()
            table_creator.get_selected_rule(table, 0)

        '''
        try:
            new_form = QtWidgets.QDialog()
            name = table.item(row, 0)
            name = name.text()
            profile = table.item(row, 2).text()
            profile = self.rules_connection.get_profiles(profile)
            direction = 1 if table.item(row, 4).text() == 'Inbound' else 2
            search = self.rules_connection.get_searched_rule(name, profile, direction)
            self.init_rule_window(new_form, True, search)
            new_form.exec_()
        except FirewallManagerError as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.message.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.message.show_message('ERROR_TablePortsCreator_Get_Rule', str(exception), self.icon)


    def setUp_filled_window(self, form: QtWidgets.QDialog, rule: list):
        '''
        Set up the window with filled information for editing a rule.

        Args:
            form (QtWidgets.QDialog): The form/window to initialize.
            rule (list): The rule data to populate the window for editing.

        Returns:
            None

        Raises:
            None

        Example Usage:
            table_creator = RulesTableCreator()
            table_creator.setUp_filled_window(form, rule)

        '''
        try:
            self.line_edit_name.setText(rule[0][0])
            self.text_edit_description.setPlainText(rule[0][6])
            if rule[0][1] == 'Yes': self.checkBox_enable.setChecked(True)
            self.comboBox_direction.setCurrentText(rule[0][4])
            self.comboBox_action.setCurrentText(rule[0][3])
            if rule[0][5] == 'TCP' or rule[0][5] == 'UDP' or rule[0][5] == 'Any':
                self.comboBox_protocol.setCurrentText(rule[0][5])
            else:
                self.comboBox_protocol.addItem(rule[0][5])
                self.comboBox_protocol.setCurrentText(rule[0][5])

            if rule[0][4] == 'Inbound':
                port_value = rule[0][7]
            else:
                port_value = rule[0][8]

            profile = rule[0][2]
            profile = self.rules_connection.get_profiles(profile)
            self.comboBox_profile.setCurrentIndex(profile)

            if port_value == '' or port_value == '*':
                self.comboBox_port.setCurrentIndex(0)
            else:
                self.comboBox_port.setCurrentIndex(1)
                self.line_edit_port.setText(port_value)

            if rule[0][9] == '':
                self.comboBox_program.setCurrentIndex(0)
            else:
                self.comboBox_program.setCurrentIndex(1)
                self.line_edit_program.setText(rule[0][9])

            if rule[0][10] != '' and rule[0][10] != '*':
                self.text_edit_IP.setPlainText(rule[0][10])

            self.btn_left.setText(self.txt_edit_btn)
            self.btn_left.clicked.connect(lambda: self.edit_selected_rule(rule))
            self.btn_left.clicked.connect(form.close)
            self.btn_right.setText(self.txt_delete_btn)
            self.btn_right.clicked.connect(lambda: self.delete_selected_rule(rule))
            self.btn_right.clicked.connect(form.close)
        except Exception as exception:
            self.message.show_message('ERROR_TablePortsCreator_Filled_Window', str(exception), self.icon)

    def edit_selected_rule(self, rule: list):
        '''
        Edit a selected firewall rule.

        Args:
            rule (list): The rule data to edit.

        Returns:
            None

        Raises:
            None

        Example Usage:
            table_creator = RulesTableCreator()
            table_creator.edit_selected_rule(rule)

        '''
        try:
            rule_data = {
                'old_name': rule[0][0],
                'old_profile': rule[0][2],
                'old_direction': rule[0][4],

                'name': self.line_edit_name.text(),
                'direction': self.comboBox_direction.currentIndex(),
                'description': self.text_edit_description.toPlainText(),
                'enable': self.checkBox_enable.isChecked(),
                'action': self.comboBox_action.currentIndex(),
                'protocol': self.comboBox_protocol.currentIndex(),
                'profile': self.comboBox_profile.currentIndex(),
                'election_port': self.comboBox_port.currentIndex(),
                'port': self.line_edit_port.text(),
                'election_program': self. comboBox_program.currentText(),
                'program': self.line_edit_program.text(),
                'ip': self.text_edit_IP.toPlainText()
            }
            self.rules_connection.edit_selected_rule(rule_data)
            self.message.show_message(self.rule_changed, '', self.icon)
        except FirewallManagerError as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.message.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.message.show_message('ERROR_RulesTableCreator_EDIT_RULE', str(exception), self.icon)

    def delete_selected_rule(self, rule: list):
        '''
        Delete a selected firewall rule.

        Args:
            rule (list): The rule data to delete.

        Returns:
            None

        Raises:
            None

        Example Usage:
            table_creator = RulesTableCreator()
            table_creator.deleteSelectedRule(rule)

        '''
        try:
            name = rule[0][0]
            direction = rule[0][4]
            profile = rule[0][2]
            protocol = rule[0][5]
            self.rules_connection.delete_selected_rule(name, direction, profile, protocol)
            self.message.show_message(self.deleted_alert, '', self.icon)
        except FirewallManagerError as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.message.show_message(error_code, error_description, self.icon_critical)
        except Exception as exception:
            self.message.show_message('ERROR_RulesTableCreator_Delete_Rule', str(exception), self.icon)
