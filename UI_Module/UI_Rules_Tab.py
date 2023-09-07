# ***************************************************
# FILE: UI_Rules_Tab.py
#
# DESCRIPTION: 
# Gets all the rules in the firewall and initialize a window with a table
# Shows more information when double click on the cell
#
# AUTHOR:  Luis Pedroza
# CREATED: 17/04/2023 (dd/mm/yy)
# ***************************************************

from PyQt5 import QtCore, QtWidgets, QtGui
from Controller_Module.Rules import Firewall_Rules
from UI_Module.UI_Message import PopUpMessage

class RulesTableCreator(object):
    #Initialize the class
    def __init__(self):
        self.message = PopUpMessage()
        self.rulesConnection = Firewall_Rules()
        self.icon = QtWidgets.QMessageBox.Information
        
    # setup of the table    
    def setup_rules_table(self, main_window, name, profile, direction):
        #initialize the main window with the specifications
        main_window.setObjectName("main_window")
        main_window.setFixedSize(760, 350)
        main_window.setWindowTitle("Búsqueda")
        main_window.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))

        # get the data 
        rules_data_list = self.rulesConnection.get_searched_rule(name, profile, direction)

        # check if data has information
        if rules_data_list:
            self.Form = QtWidgets.QWidget()
            self.new_table = QtWidgets.QTableWidget(main_window)
            header = ['Rule', 'Enable', 'Profile', 'Action', 'Direction', 'Protocol' ]
            self.new_table.setColumnCount(6)
            self.new_table.setRowCount(len(rules_data_list))
            self.new_table.setHorizontalHeaderLabels(header)
            self.new_table.setGeometry(QtCore.QRect(1, 0, 759, 511))
            self.new_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.new_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            self.new_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            self.new_table.cellDoubleClicked.connect(lambda row: self.get_selected_rule(self.new_table, row))

            # add information on the table
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

        # if there is'n data, initialize an empty table
        else: self.new_table = QtWidgets.QTableWidget(main_window)

    def init_rule_window(self, Form: QtWidgets.QDialog, action: bool=False, rule: list = None):
        '''
        if action == True the window is for edit and delete
        '''
        Form.setObjectName("Form")
        Form.setFixedSize(400, 500)
        Form.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))

        self.label_name = QtWidgets.QLabel(Form)
        self.label_name.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.label_name.setObjectName("label_name")
        self.label_name.setText("Name")
        self.line_edit_name = QtWidgets.QLineEdit(Form)
        self.line_edit_name.setGeometry(QtCore.QRect(70, 20, 291, 20))
        self.line_edit_name.setObjectName("line_edit_name")

        self.label_description = QtWidgets.QLabel(Form)
        self.label_description.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.label_description.setObjectName("label_description")
        self.label_description.setText("Description")
        self.text_edit_description = QtWidgets.QTextEdit(Form)
        self.text_edit_description.setGeometry(QtCore.QRect(20, 70, 340, 70))
        self.text_edit_description.setObjectName("text_edit_description")
        
        self.checkBox_enable = QtWidgets.QCheckBox(Form)
        self.checkBox_enable.setGeometry(QtCore.QRect(30, 160, 70, 17))
        self.checkBox_enable.setObjectName("checkBox_enable")
        self.checkBox_enable.setText("Enable")

        self.label_direction = QtWidgets.QLabel(Form)
        self.label_direction.setGeometry(QtCore.QRect(30, 200, 61, 16))
        self.label_direction.setObjectName("label_direction")
        self.label_direction.setText("Direction")
        self.comboBox_direction = QtWidgets.QComboBox(Form)
        self.comboBox_direction.setGeometry(QtCore.QRect(80, 200, 110, 22))
        self.comboBox_direction.setObjectName("comboBox_direction")
        self.comboBox_direction.addItem("Inbound")
        self.comboBox_direction.addItem("Outbound")

        self.label_action = QtWidgets.QLabel(Form)
        self.label_action.setGeometry(QtCore.QRect(30, 244, 47, 13))
        self.label_action.setObjectName("labelActionPort")
        self.label_action.setText("Acción")
        self.comboBox_action = QtWidgets.QComboBox(Form)
        self.comboBox_action.setGeometry(QtCore.QRect(80, 240, 110, 22))
        self.comboBox_action.setObjectName("comboBoxActionPort")
        self.comboBox_action.addItem("Block")
        self.comboBox_action.addItem("Allow")

        self.label_protocol = QtWidgets.QLabel(Form)
        self.label_protocol.setGeometry(QtCore.QRect(30, 284, 51, 16))
        self.label_protocol.setObjectName("label_protocol")
        self.label_protocol.setText("Protocol")
        self.comboBox_protocol = QtWidgets.QComboBox(Form)
        self.comboBox_protocol.setGeometry(QtCore.QRect(80, 280, 110, 22))
        self.comboBox_protocol.setObjectName("comboBox_protocol")
        self.comboBox_protocol.addItem("Any")
        self.comboBox_protocol.addItem("TCP")
        self.comboBox_protocol.addItem("UDP")

        self.label_port = QtWidgets.QLabel(Form)
        self.label_port.setGeometry(QtCore.QRect(210, 204, 47, 13))
        self.label_port.setObjectName("label_port")
        self.label_port.setText("Port")
        self.comboBox_port = QtWidgets.QComboBox(Form)
        self.comboBox_port.setGeometry(QtCore.QRect(260, 200, 100, 22))
        self.comboBox_port.setObjectName("comboBoxPort")
        self.comboBox_port.addItem("Any")
        self.comboBox_port.addItem("Range")
        self.line_edit_port = QtWidgets.QLineEdit(Form)
        self.line_edit_port.setGeometry(QtCore.QRect(210, 240, 150, 22))
        self.line_edit_port.setObjectName("lineEditPort")
        self.comboBox_port.currentTextChanged.connect(lambda text: self.enable_selected(text, self.line_edit_port))
        self.enable_selected(self.comboBox_port.currentText(), self.line_edit_port)

        self.label_program = QtWidgets.QLabel(Form)
        self.label_program.setGeometry(QtCore.QRect(210, 280, 51, 16))
        self.label_program.setObjectName("label_program")
        self.label_program.setText("Program")
        self.comboBox_program = QtWidgets.QComboBox(Form)
        self.comboBox_program.setGeometry(QtCore.QRect(280, 280, 80, 22))
        self.comboBox_program.setObjectName("comboBox_program")
        self.comboBox_program.addItem("Any")
        self.comboBox_program.addItem("Select")
        self.line_edit_program = QtWidgets.QLineEdit(Form)
        self.line_edit_program.setGeometry(QtCore.QRect(210, 320, 151, 20))
        self.line_edit_program.setObjectName("lineEditProgram")
        self.comboBox_program.currentTextChanged.connect(lambda text: self.enable_selected(text, self.line_edit_program))
        self.enable_selected(self.comboBox_program.currentText(), self.line_edit_program)

        self.label_IP = QtWidgets.QLabel(Form)
        self.label_IP.setGeometry(QtCore.QRect(30, 340, 100, 20))
        self.label_IP.setObjectName("label_IP")
        self.label_IP.setText("IP Direction")
        self.text_edit_IP = QtWidgets.QTextEdit(Form)
        self.text_edit_IP.setGeometry(QtCore.QRect(30, 360, 340, 70))
        self.text_edit_IP.setObjectName("text_edit_IP")      

        self.btn_left = QtWidgets.QPushButton(Form)
        self.btn_left.setGeometry(QtCore.QRect(70, 450, 101, 26))
        self.btn_left.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_left.setObjectName("btn_left")
  
        self.btn_right = QtWidgets.QPushButton(Form)
        self.btn_right.setGeometry(QtCore.QRect(250, 450, 101, 26))
        self.btn_right.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_right.setObjectName("btn_right")
        
        if action:
            self.setUp_filled_window(Form, rule)
        else:
            self.btn_left.setText("Add")
            self.btn_left.clicked.connect(self.add_new_rule)
            self.btn_left.clicked.connect(Form.close)
            self.btn_right.setText("Cancel")
            self.btn_right.clicked.connect(Form.close)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Rule"))
    
    def enable_selected(self, text, line_edit_widget):
        if text == 'Any':
            line_edit_widget.setEnabled(False)
        else:
            line_edit_widget.setEnabled(True)

    def add_new_rule(self):
        name = self.line_edit_name.text()
        if name != '':
            description = self.text_edit_description.toPlainText()
            enable = self.checkBox_enable.isChecked()
            direction = self.comboBox_direction.currentText()
            action = self.comboBox_action.currentText()
            protocol = self.comboBox_protocol.currentText()
            protocol = None if protocol == 'Any' else protocol
            port = self.comboBox_port.currentText()
            program = self.comboBox_program.currentText()
            ip = self.text_edit_IP.toPlainText()
            selected_port = None if port == 'Any' else self.line_edit_port.text()
            selected_program = None if program == 'Any' else self.line_edit_program.text()

            self.rulesConnection.add_new_rule(name, description, enable, direction, action, protocol, selected_port, selected_program, ip)
        else:
            code = 'specify the name of the rule'
            error = 'To create a new rule you must specify at least the name of the rule.\n Check help to create a new rule'
            self.message.show_message(code, error, self.icon)

    def get_selected_rule(self, table: QtWidgets.QTableWidget, row: int):
            new_form = QtWidgets.QDialog()
            name = table.item(row, 0)
            name = name.text()
            profile = table.item(row, 2)
            profile = profile.text()
            direction = table.item(row, 4)
            direction = direction.text()

            search = self.rulesConnection.get_searched_rule(name, profile, direction)
            self.init_rule_window(new_form, True, search)
            new_form.exec_()

    def setUp_filled_window(self, form: QtWidgets.QDialog, rule: list):
        try:
            self.line_edit_name.setText(rule[0][0])
            self.text_edit_description.setPlainText(rule[0][6])
            if rule[0][1] == 'Yes': self.checkBox_enable.setChecked(True)
            self.comboBox_direction.setCurrentText(rule[0][4])
            self.comboBox_action.setCurrentText(rule[0][3])
            if rule[0][5] == 'TCP' or rule[0][5] == 'UDP':
                self.comboBox_protocol.setCurrentText(rule[0][5])
            else:
                self.comboBox_protocol.addItem(rule[0][5])
                self.comboBox_protocol.setCurrentText(rule[0][5])

            if rule[0][4] == 'Inbound':
                port_value = rule[0][7]
            else:
                port_value = rule[0][8]

            if port_value == '' or port_value == '*':
                self.comboBox_port.setCurrentText('Any')
            else:
                self.comboBox_port.setCurrentText('Range')
                self.line_edit_port.setText(port_value)

            if rule[0][9] == '':
                self.comboBox_program.setCurrentIndex(0)
            else:
                self.comboBox_program.setCurrentIndex(1)
                self.line_edit_program.setText(rule[0][9])

            if rule[0][10] != '' and rule[0][10] != '*':
                self.text_edit_IP.setPlainText(rule[0][10])

            self.btn_left.setText("Edit")
            self.btn_left.clicked.connect(lambda: self.edit_selected_rule(rule))
            self.btn_left.clicked.connect(form.close)
            self.btn_right.setText("Delete")
            # self.btn_right.clicked.connect(self.deleteSelectedRule())

            self.retranslateUi(form)
            QtCore.QMetaObject.connectSlotsByName(form)
        except Exception as exception:
            code = 'No se pudo acceder a la regla seleccionada'
            self.message.show_message(code, exception, self.icon)

    def edit_selected_rule(self, rule: list):
        old_name = rule[0][0]
        profile = rule[0][2]
        old_direction = rule[0][4]

        name = self.line_edit_name.text()
        direction = self.comboBox_direction.currentText()
        description = self.text_edit_description.toPlainText()
        enable = self.checkBox_enable.isChecked()
        action = self.comboBox_action.currentText()
        protocol = self.comboBox_protocol.currentText()
        election_port = self.comboBox_port.currentText()
        port = self.line_edit_port.text()
        election_program = self. comboBox_program.currentText()
        program = self.line_edit_program.text()
        ip = self.text_edit_IP.toPlainText()
        self.rulesConnection.edit_selected_rule(old_name, profile, old_direction, name, description, enable, direction, action, protocol, port, election_port,  program, election_program, ip)

    # Method to delete the selected rule
    def deleteSelectedRule(self):
        pass