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
        rules_data_list = self.rulesConnection.searchRules(name, profile, direction)

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

    def init_rule_window(self, Form:QtWidgets.QDialog, action:bool=False):
        '''
        if action == True the window is for edit and delete
        '''
        Form.setObjectName("Form")
        Form.setFixedSize(400, 500)
        Form.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))

        self.label_name = QtWidgets.QLabel(Form)
        self.label_name.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.label_name.setObjectName("label_name")
        self.label_name.setText("Nombre")
        self.line_edit_name = QtWidgets.QLineEdit(Form)
        self.line_edit_name.setGeometry(QtCore.QRect(70, 20, 291, 20))
        self.line_edit_name.setObjectName("line_edit_name")

        self.label_description = QtWidgets.QLabel(Form)
        self.label_description.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.label_description.setObjectName("label_description")
        self.label_description.setText("Descripción")
        self.text_edit_description = QtWidgets.QTextEdit(Form)
        self.text_edit_description.setGeometry(QtCore.QRect(20, 70, 340, 70))
        self.text_edit_description.setObjectName("text_edit_description")
        
        self.check_box_enable = QtWidgets.QCheckBox(Form)
        self.check_box_enable.setGeometry(QtCore.QRect(30, 160, 70, 17))
        self.check_box_enable.setObjectName("check_box_enable")
        self.check_box_enable.setText("Habilitada")

        self.label_direction = QtWidgets.QLabel(Form)
        self.label_direction.setGeometry(QtCore.QRect(30, 200, 61, 16))
        self.label_direction.setObjectName("label_direction")
        self.label_direction.setText("Dirección")
        self.comboBox_direction = QtWidgets.QComboBox(Form)
        self.comboBox_direction.setGeometry(QtCore.QRect(80, 200, 110, 22))
        self.comboBox_direction.setObjectName("comboBox_direction")
        self.comboBox_direction.addItem("Entrada")
        self.comboBox_direction.addItem("Salida")

        self.label_action = QtWidgets.QLabel(Form)
        self.label_action.setGeometry(QtCore.QRect(30, 244, 47, 13))
        self.label_action.setObjectName("labelActionPort")
        self.label_action.setText("Acción")
        self.comboBox_action = QtWidgets.QComboBox(Form)
        self.comboBox_action.setGeometry(QtCore.QRect(80, 240, 110, 22))
        self.comboBox_action.setObjectName("comboBoxActionPort")
        self.comboBox_action.addItem("Bloquear")
        self.comboBox_action.addItem("Permitir")

        self.label_protocol = QtWidgets.QLabel(Form)
        self.label_protocol.setGeometry(QtCore.QRect(30, 284, 51, 16))
        self.label_protocol.setObjectName("label_protocol")
        self.label_protocol.setText("Protocolo")
        self.comboBox_protocol = QtWidgets.QComboBox(Form)
        self.comboBox_protocol.setGeometry(QtCore.QRect(80, 280, 110, 22))
        self.comboBox_protocol.setObjectName("comboBox_protocol")
        self.comboBox_protocol.addItem("Todos")
        self.comboBox_protocol.addItem("TCP")
        self.comboBox_protocol.addItem("UDP")

        self.label_port = QtWidgets.QLabel(Form)
        self.label_port.setGeometry(QtCore.QRect(210, 204, 47, 13))
        self.label_port.setObjectName("label_port")
        self.label_port.setText("Puerto")
        self.comboBox_port = QtWidgets.QComboBox(Form)
        self.comboBox_port.setGeometry(QtCore.QRect(260, 200, 100, 22))
        self.comboBox_port.setObjectName("comboBoxPort")
        self.comboBox_port.addItem("Todos")
        self.comboBox_port.addItem("Rango")
        self.line_edit_port = QtWidgets.QLineEdit(Form)
        self.line_edit_port.setGeometry(QtCore.QRect(210, 240, 150, 22))
        self.line_edit_port.setObjectName("lineEditPort")
        self.comboBox_port.currentTextChanged.connect(lambda text: self.enable_selected(text, self.line_edit_port))
        self.enable_selected(self.comboBox_port.currentText(), self.line_edit_port)

        self.label_program = QtWidgets.QLabel(Form)
        self.label_program.setGeometry(QtCore.QRect(210, 280, 51, 16))
        self.label_program.setObjectName("label_program")
        self.label_program.setText("Programa")
        self.comboBox_program = QtWidgets.QComboBox(Form)
        self.comboBox_program.setGeometry(QtCore.QRect(280, 280, 80, 22))
        self.comboBox_program.setObjectName("comboBox_program")
        self.comboBox_program.addItem("Todos")
        self.comboBox_program.addItem("Seleccionar")
        self.line_edit_program = QtWidgets.QLineEdit(Form)
        self.line_edit_program.setGeometry(QtCore.QRect(210, 320, 151, 20))
        self.line_edit_program.setObjectName("lineEditProgram")
        self.comboBox_program.currentTextChanged.connect(lambda text: self.enable_selected(text, self.line_edit_program))
        self.enable_selected(self.comboBox_program.currentText(), self.line_edit_program)

        self.label_IP = QtWidgets.QLabel(Form)
        self.label_IP.setGeometry(QtCore.QRect(30, 340, 100, 20))
        self.label_IP.setObjectName("label_IP")
        self.label_IP.setText("Dirección IP")
        self.text_edit_IP = QtWidgets.QTextEdit(Form)
        self.text_edit_IP.setGeometry(QtCore.QRect(30, 360, 340, 70))
        self.text_edit_IP.setObjectName("text_edit_IP")      

        self.btn_edit_rule = QtWidgets.QPushButton(Form)
        self.btn_edit_rule.setGeometry(QtCore.QRect(70, 450, 101, 26))
        self.btn_edit_rule.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_edit_rule.setObjectName("btn_edit_rule")
        self.btn_edit_rule.setText("Editar")
        self.btn_delete_rule = QtWidgets.QPushButton(Form)
        self.btn_delete_rule.setGeometry(QtCore.QRect(250, 450, 101, 26))
        self.btn_delete_rule.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_rule.setObjectName("btn_delete_rule")
        self.btn_delete_rule.setText("Eliminar")
        
        if action:
            self.setUp_filled_window(Form)
        else:
            self.btn_edit_rule.setText("Agregar")
            self.btn_edit_rule.clicked.connect(self.add_new_rule)
            self.btn_edit_rule.clicked.connect(Form.close)
            self.btn_delete_rule.setText("Cancelar")
            self.btn_delete_rule.clicked.connect(Form.close)
            self.retranslateUi(Form)
            QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Regla"))
    
    def enable_selected(self, text, line_edit_widget):
        if text == 'Todos':
            line_edit_widget.setEnabled(False)
        else:
            line_edit_widget.setEnabled(True)

    def add_new_rule(self):
        name = self.line_edit_name.text()
        if name != '':
            description = self.text_edit_description.toPlainText()
            enable = 'yes' if self.check_box_enable.isChecked() else 'no'
            direction = 'in' if self.comboBox_direction.currentText() == 'Entrada' else 'out'
            action = 'allow' if self.comboBox_action.currentText() == 'Permitir' else 'block'
            protocol = self.comboBox_protocol.currentText()
            protocol = None if protocol == 'Todos' else protocol
            port = self.comboBox_port.currentText()
            program = self.comboBox_program.currentText()
            ip = self.text_edit_IP.toPlainText()
            selected_port = None if port == 'Todos' else self.line_edit_port.text()
            selected_program = None if program == 'Todos' else self.line_edit_program.text()

            self.rulesConnection.addRule(name, description, enable, direction, action, protocol, selected_port, selected_program, ip)
        else:
            code = 'No ingresó el nombre de la regla'
            error = 'Debe ingresar el nombre de la regla.\nRevise la ayuda para crear nuevas reglas'
            self.message.show_message(code, error, self.icon)

    def get_selected_rule(self, table: QtWidgets.QTableWidget, row: int):
            newForm = QtWidgets.QDialog()
            name = table.item(row, 0)
            profile = table.item(row, 2)
            direction = table.item(row, 4)
            protocol = table.item(row, 5)
            print(name.text())
            print(profile.text())
            print(direction.text())
            print(protocol.text())

            #search = self.rulesConnection.searchRules(name, profile, direction)
            #self.setUp_filled_window(newForm, True)

    def setUp_filled_window(self, protocol, form):
        self.labelProfile = QtWidgets.QLabel(self.tabPort)
        self.labelProfile.setGeometry(QtCore.QRect(30, 280, 47, 13))
        self.labelProfile.setObjectName("labelProfile")
        self.labelProfile.setText("Perfil")

        self.checkBoxPrivate = QtWidgets.QCheckBox(self.tabPort)
        self.checkBoxPrivate.setGeometry(QtCore.QRect(30, 300, 70, 17))
        self.checkBoxPrivate.setObjectName("checkBoxPrivate")
        self.checkBoxPrivate.setText("Privada")
        self.checkBoxPublic = QtWidgets.QCheckBox(self.tabPort)
        self.checkBoxPublic.setGeometry(QtCore.QRect(30, 330, 70, 17))
        self.checkBoxPublic.setObjectName("checkBoxPublic")
        self.checkBoxPublic.setText("Pública")
        self.checkBoxDomain = QtWidgets.QCheckBox(self.tabPort)
        self.checkBoxDomain.setGeometry(QtCore.QRect(30, 360, 70, 17))
        self.checkBoxDomain.setObjectName("checkBoxDomain")
        self.checkBoxDomain.setText("Dominio")
        try:
            self.lineEditName.setText(self.get_rule_list[0]['Nombre de regla'])
            self.comboBoxDirection.setCurrentText(self.get_rule_list[0]['Dirección'])
            self.comboBoxAction.setCurrentText(self.get_rule_list[0]['Acción'])
            self.comboBoxProtocol.setCurrentText(protocol)

            if 'Descripción' in self.get_rule_list[0]:
                self.textEditDescription.setText(self.get_rule_list[0]['Descripción'])
            else: self.textEditDescription.setText('None')

            if 'LocalPort' in self.getRule[0] or 'RemotePort' in self.getRule[0]:
                if self.getRule[0]['LocalPort'] != 'Cualquiera':
                    self.comboBoxPort.setCurrentText('Rango')
                    self.lineEditPort.setText(self.getRule[0]['LocalPort'])
                elif self.getRule[0]['RemotePort'] != 'Cualquiera':
                    self.comboBoxPort.setCurrentText('Rango')
                    self.lineEditPort.setText(self.getRule[0]['RemotePort'])
                else:
                    self.comboBoxPort.setCurrentText('Todos')
            else: 
                self.comboBoxPort.setCurrentText('Todos')
                self.comboBoxProtocol.addItem(self.getRule[0]['Protocolo'])
                self.comboBoxProtocol.setCurrentText(self.getRule[0]['Protocolo'])
                self.comboBoxProtocol.setEnabled(False)
                self.comboBoxPort.setEnabled(False)
                self.lineEditPort.setEnabled(False)

            if self.getRule[0]['Habilitada'] == 'Sí':
                self.checkBoxEnable.setChecked(True)

            valueProfile = self.getRule[0]['Perfiles'].split(',')
            for profile in valueProfile:
                if profile == "Public":
                    self.checkBoxPublic.setChecked(True)
                elif profile == "Private":
                    self.checkBoxPrivate.setChecked(True)
                elif profile == "Domain":
                    self.checkBoxDomain.setChecked(True)

            self.btnEdit.setText("Editar")
            self.btnEdit.clicked.connect(self.editSelectedRule)
            self.btnDelete.setText("Eliminar")
            self.btnDelete.clicked.connect(self.deleteSelectedRule)

            self.retranslateUi(form)
            QtCore.QMetaObject.connectSlotsByName(form)
            return True
        except Exception as exception:
            code = 'No se pudo acceder a la regla seleccionada'
            self.message.show_message(code, exception, self.icon)
            return False

    # Method to delete the selected rule
    def deleteSelectedRule(self):
        pass
        mainMessage = QtWidgets.QMessageBox()
        mainMessage.setWindowTitle('AVISO')
        mainMessage.setText('Se eliminará la regla seleccionada')
        mainMessage.setInformativeText('¿Desea continuar?')
        mainMessage.setIcon(QtWidgets.QMessageBox.Question)
        mainMessage.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        buttonYes = mainMessage.button(QtWidgets.QMessageBox.Yes)
        buttonYes.setText("Sí")
        mainMessage.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        # translations of the profile
        translations = {
        "Pública": "public",
        "Privada": "private",
        "Dominio": "domain",
        }
        # try for when the rule is'nt a port rule
        try:
            # Get the rule data
            name = self.getRule[0]['Nombre de regla']
            direction = 'in' if self.getRule[0]['Dirección'] == 'Dentro' else 'out'
            protocol = self.getRule[0]['Protocolo']
            profile = self.getRule[0]['Perfiles']
            values = profile.split(",")
            translated_values = [translations[value.strip()] if value.strip() in translations else value.strip() for value in values]
            translated_value = ",".join(translated_values)
            profile = translated_value

            # Get the port, it could be local, remote or any
            if 'LocalPort' in self.getRule[0] or 'RemotePort' in self.getRule[0]:
                if self.getRule[0]['LocalPort'] != 'Cualquiera':
                    port = f"LocalPort={self.getRule[0]['LocalPort']}"
                elif self.getRule[0]['RemotePort'] != 'Cualquiera':
                    port = f"RemotePort={self.getRule[0]['RemotePort']}"
                else:
                    port = None
            result=mainMessage.exec_()
            # Confirm the action and delete the rule
            if result == QtWidgets.QMessageBox.Yes:
                self.rulesConnection.deleteRule(name, direction, profile, protocol.lower(), port)
        except Exception as exception:
                code = 'Ocurrió un error'
                self.message.show_message(code, exception, self.icon)

    # Edit the selected rule
    def editSelectedRule(self):
        pass
        # NOTE: CHECK IF THE lineEditPort HAS AN ACCEPTABLE VALUE
        oldName = self.getRule[0]['Nombre de regla']
        oldDirection = 'in' if self.getRule[0]['Dirección'] == 'Dentro' else 'out'
        oldProtocol = 'any' if self.getRule[0]['Protocolo'] == 'Cualquiera' else self.getRule[0]['Protocolo']
        name = self.lineEditName.text()
        # Check if name has a value
        if name != "":
            description = self.textEditDescription.toPlainText()
            protocol = 'any' if self.comboBoxProtocol.currentText() == 'Cualquiera' else self.comboBoxProtocol.currentText()
            selectedPort = self.comboBoxPort.currentText()
            direction = 'in' if self.comboBoxDirection.currentText() == 'Dentro' else 'out'
            enable = 'yes' if self.checkBoxEnable.isChecked() else 'no'
            action = 'allow' if self.comboBoxAction.currentText() == 'Permitir' else \
            'block' if self.comboBoxAction.currentText() == 'Bloquear' else ''
            profile = ','.join([profile for profile, check_box in {'private': self.checkBoxPrivate, 'public': self.checkBoxPublic, 'domain': self.checkBoxDomain}.items() if check_box.isChecked()]) or 'any'
            # Check the port and the direction            
            if direction == 'in':
                if selectedPort == 'Todos':
                    port = 'localport=any remoteport=any'
                else:
                    port = f'localport={self.lineEditPort.text()}'
            elif direction == 'out':
                if selectedPort == 'Todos':
                    port = 'localport=any remoteport=any'
                else:
                    port = f'remoteport={self.lineEditPort.text()}'
            self.rulesConnection.editRule(oldName, oldDirection, oldProtocol.lower() ,name, direction, action, protocol.lower(), port, profile, description, enable)
        # Exception if name is empty
        else:
            code = 'Debe especificar un nombre'
            error = 'Debe especificar el nombre de la regla.\nRevise la ayuda para modificar nuevas reglas'
            self.message.show_message(code, error, self.icon)

    