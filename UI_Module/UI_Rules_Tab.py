
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
from UI_Module.UI_Error import PopUp_Messages

class RulesTable_Creator(object):
    #Initialize the class
    def __init__(self, name='', profile='', direction=''):
        self.message = PopUp_Messages()
        self.rulesConnection = Firewall_Rules()
        self.icon = QtWidgets.QMessageBox.Information
        self.name = name
        self.profile = profile
        self.direction= direction
        
    # setup of the table    
    def setupTable(self, MainWindow):
        #initialize the main window with the specifications
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(760, 350)
        MainWindow.setWindowTitle("Búsqueda")
        MainWindow.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))

        # get the data 
        dataList = self.rulesConnection.searchRules(self.name, self.profile, self.direction)

        # check if data has information
        if dataList:
            self.Form = QtWidgets.QWidget()
            self.newTable = QtWidgets.QTableWidget(MainWindow)
            header = ['Regla', 'Habilitada', 'Perfil', 'Acción', 'Dirección', 'Protocolo' ]
            self.newTable.setColumnCount(6)
            self.newTable.setRowCount(len(dataList))
            self.newTable.setHorizontalHeaderLabels(header)
            self.newTable.setGeometry(QtCore.QRect(1, 0, 759, 511))
            self.newTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.newTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            self.newTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            self.newTable.cellDoubleClicked.connect(self.getSelectedRule)

            # add information on the table
            for i, row in enumerate(dataList):
                item = QtWidgets.QTableWidgetItem(str(row["Nombre de regla"]))
                self.newTable.setItem(i, 0, item)
                item = QtWidgets.QTableWidgetItem(str(row["Habilitada"]))
                self.newTable.setItem(i, 1, item)
                item = QtWidgets.QTableWidgetItem(str(row["Perfiles"]))
                self.newTable.setItem(i, 2, item)
                item = QtWidgets.QTableWidgetItem(str(row["Acción"]))
                self.newTable.setItem(i, 3, item)
                item = QtWidgets.QTableWidgetItem(str(row["Dirección"]))
                self.newTable.setItem(i, 4, item)
                item = QtWidgets.QTableWidgetItem(str(row["Protocolo"]))
                self.newTable.setItem(i, 5, item)

        # if there is'n data, initialize an empty table
        else: self.newTable = QtWidgets.QTableWidget(MainWindow)

    def initRuleWindow(self, Form, protocol=None, rule=None, action=False):
        '''
        if action == True the window is for edit and delete
        '''
        self.getRule  = rule
        Form.setObjectName("Form")
        Form.setFixedSize(400, 476)
        Form.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))

        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 401, 471))
        self.tabWidget.setObjectName("tabWidget")
        #************************* TAB PORTS **************************"
        self.tabPort = QtWidgets.QWidget()
        self.tabPort.setObjectName("tabPort")

        self.labelNamePort = QtWidgets.QLabel(self.tabPort)
        self.labelNamePort.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.labelNamePort.setObjectName("labelNamePort")
        self.labelNamePort.setText("Nombre")
        self.lineEditNamePort = QtWidgets.QLineEdit(self.tabPort)
        self.lineEditNamePort.setGeometry(QtCore.QRect(70, 20, 291, 20))
        self.lineEditNamePort.setObjectName("lineEditNamePort")

        self.labelDescriptionPort = QtWidgets.QLabel(self.tabPort)
        self.labelDescriptionPort.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.labelDescriptionPort.setObjectName("labelDescriptionPort")
        self.labelDescriptionPort.setText("Descripción")
        self.textEditDescriptionPort = QtWidgets.QTextEdit(self.tabPort)
        self.textEditDescriptionPort.setGeometry(QtCore.QRect(20, 70, 341, 71))
        self.textEditDescriptionPort.setObjectName("textEditDescriptionPort")
        
        self.checkBoxEnablePort = QtWidgets.QCheckBox(self.tabPort)
        self.checkBoxEnablePort.setGeometry(QtCore.QRect(30, 160, 70, 17))
        self.checkBoxEnablePort.setObjectName("checkBoxEnablePort")
        self.checkBoxEnablePort.setText("Habilitada")

        self.labelDirectionPort = QtWidgets.QLabel(self.tabPort)
        self.labelDirectionPort.setGeometry(QtCore.QRect(30, 200, 61, 16))
        self.labelDirectionPort.setObjectName("labelDirectionPort")
        self.labelDirectionPort.setText("Dirección")
        self.comboBoxDirectionPort = QtWidgets.QComboBox(self.tabPort)
        self.comboBoxDirectionPort.setGeometry(QtCore.QRect(80, 200, 69, 22))
        self.comboBoxDirectionPort.setObjectName("comboBoxDirectionPort")
        self.comboBoxDirectionPort.addItem("Dentro")
        self.comboBoxDirectionPort.addItem("Fuera")

        self.labelActionPort = QtWidgets.QLabel(self.tabPort)
        self.labelActionPort.setGeometry(QtCore.QRect(30, 244, 47, 13))
        self.labelActionPort.setObjectName("labelActionPort")
        self.labelActionPort.setText("Acción")
        self.comboBoxActionPort = QtWidgets.QComboBox(self.tabPort)
        self.comboBoxActionPort.setGeometry(QtCore.QRect(80, 240, 110, 22))
        self.comboBoxActionPort.setObjectName("comboBoxActionPort")
        self.comboBoxActionPort.addItem("Bloquear")
        self.comboBoxActionPort.addItem("Permitir")

        self.labelProtocol = QtWidgets.QLabel(self.tabPort)
        self.labelProtocol.setGeometry(QtCore.QRect(210, 200, 51, 16))
        self.labelProtocol.setObjectName("labelProtocol")
        self.labelProtocol.setText("Protocolo")
        self.comboBoxProtocol = QtWidgets.QComboBox(self.tabPort)
        self.comboBoxProtocol.setGeometry(QtCore.QRect(280, 200, 80, 22))
        self.comboBoxProtocol.setObjectName("comboBoxProtocol")
        self.comboBoxProtocol.addItem("TCP")
        self.comboBoxProtocol.addItem("UDP")

        self.labelPort = QtWidgets.QLabel(self.tabPort)
        self.labelPort.setGeometry(QtCore.QRect(210, 244, 47, 13))
        self.labelPort.setObjectName("labelPort")
        self.labelPort.setText("Puerto")
        self.comboBoxPort = QtWidgets.QComboBox(self.tabPort)
        self.comboBoxPort.setGeometry(QtCore.QRect(280, 240, 80, 22))
        self.comboBoxPort.setObjectName("comboBoxPort")
        self.comboBoxPort.addItem("Todos")
        self.comboBoxPort.addItem("Rango")
        self.lineEditPort = QtWidgets.QLineEdit(self.tabPort)
        self.lineEditPort.setGeometry(QtCore.QRect(210, 290, 151, 20))
        self.lineEditPort.setObjectName("lineEditPort")
        self.comboBoxPort.currentTextChanged.connect(lambda text: self.enableSelected(text, self.lineEditPort))
        self.enableSelected(self.comboBoxPort.currentText(), self.lineEditPort)
        
        self.tabWidget.addTab(self.tabPort, "")        
        #************************* TAB PROGRAM **************************"
        self.tabProgram = QtWidgets.QWidget()
        self.tabProgram.setObjectName("tabProgram")

        self.labelNameProgram = QtWidgets.QLabel(self.tabProgram)
        self.labelNameProgram.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.labelNameProgram.setObjectName("labelNameProgram")
        self.labelNameProgram.setText("Nombre")
        self.lineEditNameProgram = QtWidgets.QLineEdit(self.tabProgram)
        self.lineEditNameProgram.setGeometry(QtCore.QRect(70, 20, 291, 20))
        self.lineEditNameProgram.setObjectName("lineEditNameProgram")

        self.labelDescriptionProgram = QtWidgets.QLabel(self.tabProgram)
        self.labelDescriptionProgram.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.labelDescriptionProgram.setObjectName("labelDescriptionProgram")
        self.labelDescriptionProgram.setText("Descripción")
        self.textEditDescriptionProgram = QtWidgets.QTextEdit(self.tabProgram)
        self.textEditDescriptionProgram.setGeometry(QtCore.QRect(20, 70, 341, 71))
        self.textEditDescriptionProgram.setObjectName("textEditDescriptionProgram")
        
        self.checkBoxEnableProgram = QtWidgets.QCheckBox(self.tabProgram)
        self.checkBoxEnableProgram.setGeometry(QtCore.QRect(30, 160, 70, 17))
        self.checkBoxEnableProgram.setObjectName("checkBoxEnableProgram")
        self.checkBoxEnableProgram.setText("Habilitada")

        self.labelDirectionProgram = QtWidgets.QLabel(self.tabProgram)
        self.labelDirectionProgram.setGeometry(QtCore.QRect(30, 200, 61, 16))
        self.labelDirectionProgram.setObjectName("labelDirectionProgram")
        self.labelDirectionProgram.setText("Dirección")
        self.comboBoxDirectionProgram = QtWidgets.QComboBox(self.tabProgram)
        self.comboBoxDirectionProgram.setGeometry(QtCore.QRect(80, 200, 69, 22))
        self.comboBoxDirectionProgram.setObjectName("comboBoxDirectionProgram")
        self.comboBoxDirectionProgram.addItem("Dentro")
        self.comboBoxDirectionProgram.addItem("Fuera")

        self.labelActionProgram = QtWidgets.QLabel(self.tabProgram)
        self.labelActionProgram.setGeometry(QtCore.QRect(30, 244, 47, 13))
        self.labelActionProgram.setObjectName("labelActionProgram")
        self.labelActionProgram.setText("Acción")
        self.comboBoxActionProgram = QtWidgets.QComboBox(self.tabProgram)
        self.comboBoxActionProgram.setGeometry(QtCore.QRect(80, 240, 110, 22))
        self.comboBoxActionProgram.setObjectName("comboBoxActionProgram")
        self.comboBoxActionProgram.addItem("Bloquear")
        self.comboBoxActionProgram.addItem("Permitir")

        self.labelProgram = QtWidgets.QLabel(self.tabProgram)
        self.labelProgram.setGeometry(QtCore.QRect(210, 200, 51, 16))
        self.labelProgram.setObjectName("labelProgram")
        self.labelProgram.setText("Programa")
        self.comboBoxProgram = QtWidgets.QComboBox(self.tabProgram)
        self.comboBoxProgram.setGeometry(QtCore.QRect(280, 200, 80, 22))
        self.comboBoxProgram.setObjectName("comboBoxProgram")
        self.comboBoxProgram.addItem("Todos")
        self.comboBoxProgram.addItem("Seleccionar")
        self.lineEditProgram = QtWidgets.QLineEdit(self.tabProgram)
        self.lineEditProgram.setGeometry(QtCore.QRect(210, 240, 151, 20))
        self.lineEditProgram.setObjectName("lineEditProgram")
        self.comboBoxProgram.currentTextChanged.connect(lambda text: self.enableSelected(text, self.lineEditProgram))
        self.enableSelected(self.comboBoxProgram.currentText(), self.lineEditProgram)

        self.tabWidget.addTab(self.tabProgram, "Programa")
        #************************* TAB IP **************************"
        self.tabIP = QtWidgets.QWidget()
        self.tabIP.setObjectName("tabIP")
        
        self.labelNameIP = QtWidgets.QLabel(self.tabIP)
        self.labelNameIP.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.labelNameIP.setObjectName("labelNameIP")
        self.labelNameIP.setText("Nombre")
        self.lineEditNameIP = QtWidgets.QLineEdit(self.tabIP)
        self.lineEditNameIP.setGeometry(QtCore.QRect(70, 20, 291, 20))
        self.lineEditNameIP.setObjectName("lineEditNameIP")

        self.labelDescriptionIP = QtWidgets.QLabel(self.tabIP)
        self.labelDescriptionIP.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.labelDescriptionIP.setObjectName("labelDescriptionIP")
        self.labelDescriptionIP.setText("Descripción")
        self.textEditDescriptionIP = QtWidgets.QTextEdit(self.tabIP)
        self.textEditDescriptionIP.setGeometry(QtCore.QRect(20, 70, 341, 71))
        self.textEditDescriptionIP.setObjectName("textEditDescriptionIP")
        
        self.checkBoxEnableIP = QtWidgets.QCheckBox(self.tabIP)
        self.checkBoxEnableIP.setGeometry(QtCore.QRect(30, 160, 70, 17))
        self.checkBoxEnableIP.setObjectName("checkBoxEnableIP")
        self.checkBoxEnableIP.setText("Habilitada")

        self.labelDirectionIP = QtWidgets.QLabel(self.tabIP)
        self.labelDirectionIP.setGeometry(QtCore.QRect(30, 200, 61, 16))
        self.labelDirectionIP.setObjectName("labelDirectionIP")
        self.labelDirectionIP.setText("Dirección")
        self.comboBoxDirectionIP = QtWidgets.QComboBox(self.tabIP)
        self.comboBoxDirectionIP.setGeometry(QtCore.QRect(80, 200, 69, 22))
        self.comboBoxDirectionIP.setObjectName("comboBoxDirectionIP")
        self.comboBoxDirectionIP.addItem("Dentro")
        self.comboBoxDirectionIP.addItem("Fuera")

        self.labelActionIP = QtWidgets.QLabel(self.tabIP)
        self.labelActionIP.setGeometry(QtCore.QRect(30, 244, 47, 13))
        self.labelActionIP.setObjectName("labelActionIP")
        self.labelActionIP.setText("Acción")
        self.comboBoxActionIP = QtWidgets.QComboBox(self.tabIP)
        self.comboBoxActionIP.setGeometry(QtCore.QRect(80, 240, 110, 22))
        self.comboBoxActionIP.setObjectName("comboBoxActionIP")
        self.comboBoxActionIP.addItem("Bloquear")
        self.comboBoxActionIP.addItem("Permitir")

        self.labelProgramIP = QtWidgets.QLabel(self.tabIP)
        self.labelProgramIP.setGeometry(QtCore.QRect(210, 200, 51, 16))
        self.labelProgramIP.setObjectName("labelProgramIP")
        self.labelProgramIP.setText("Programa")
        self.comboBoxProgramIP = QtWidgets.QComboBox(self.tabIP)
        self.comboBoxProgramIP.setGeometry(QtCore.QRect(280, 200, 80, 22))
        self.comboBoxProgramIP.setObjectName("comboBoxProgramIP")
        self.comboBoxProgramIP.addItem("Todos")
        self.comboBoxProgramIP.addItem("Seleccionar")
        self.lineEditProgramIP = QtWidgets.QLineEdit(self.tabIP)
        self.lineEditProgramIP.setGeometry(QtCore.QRect(210, 240, 151, 20))
        self.lineEditProgramIP.setObjectName("lineEditProgramIP")
        self.comboBoxProgramIP.currentTextChanged.connect(lambda text: self.enableSelected(text, self.lineEditProgramIP))
        self.enableSelected(self.comboBoxProgramIP.currentText(), self.lineEditProgramIP)

        self.labelIP = QtWidgets.QLabel(self.tabIP)
        self.labelIP.setGeometry(QtCore.QRect(30, 280, 100, 20))
        self.labelIP.setObjectName("labelIP")
        self.labelIP.setText("Dirección IP")
        self.textEditIP = QtWidgets.QTextEdit(self.tabIP)
        self.textEditIP.setGeometry(QtCore.QRect(30, 300, 341, 71))
        self.textEditIP.setObjectName("textEditIP")

        self.tabWidget.addTab(self.tabIP, "IP")

        self.btnEdit = QtWidgets.QPushButton(self.tabWidget)
        self.btnEdit.setGeometry(QtCore.QRect(70, 420, 101, 26))
        self.btnEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnEdit.setObjectName("btnEdit")
        self.btnEdit.setText("Editar")
        self.btnDelete = QtWidgets.QPushButton(self.tabWidget)
        self.btnDelete.setGeometry(QtCore.QRect(250, 420, 101, 26))
        self.btnDelete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnDelete.setObjectName("btnDelete")
        self.btnDelete.setText("Eliminar")
        
        if action:
            check = self.setUpFilledWindow(protocol)
            if check:
                self.retranslateUi(Form)
                self.tabWidget.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(Form)
                Form.exec_()
        else:
            self.btnEdit.setText("Agregar")
            self.btnEdit.clicked.connect(self.addNewRule)
            self.btnEdit.clicked.connect(Form.close)
            self.btnDelete.setText("Cancelar")
            self.btnDelete.clicked.connect(Form.close)
            self.retranslateUi(Form)
            self.tabWidget.setCurrentIndex(0)
            QtCore.QMetaObject.connectSlotsByName(Form)
            Form.exec_()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Regla"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPort), _translate("Form", "Puerto"))
    
    def enableSelected(self, text, line_edit_widget):
        if text == 'Todos':
            line_edit_widget.setEnabled(False)
        else:
            line_edit_widget.setEnabled(True)

    def addNewRule(self):
        currentTab = self.tabWidget.currentIndex()
        if currentTab == 0:
            self.addPortRule()
        elif currentTab == 1:
            self.addProgramRule()
        elif currentTab == 2:
            self.addIpRule()

    def addPortRule(self):
        name = self.lineEditNamePort.text()
        # Check if the name is'nt empty
        if name != '':
            description = self.textEditDescriptionPort.toPlainText()
            protocol = self.comboBoxProtocol.currentText()
            port = self.comboBoxPort.currentText()
            direction = 'in' if self.comboBoxDirectionPort.currentText() == 'Dentro' else 'out'
            enable = 'yes' if self.checkBoxEnablePort.isChecked() else 'no'
            action = 'allow' if self.comboBoxActionPort.currentText() == 'Permitir' else 'block'
            if direction == 'in':
                if port == 'Todos':
                    selectedPort = None
                else:
                    selectedPort = self.lineEditPort.text()
            elif direction == 'out':
                if port == 'Todos':
                    selectedPort = None
                else:
                    selectedPort = self.lineEditPort.text()
            self.rulesConnection.addRule(name, direction, action, protocol, description, enable, port=selectedPort)
        # exception if name is empty
        else:
            code = 'No ingresó el nombre de la regla'
            error = 'Debe ingresar el nombre de la regla.\nRevise la ayuda para crear nuevas reglas'
            self.message.showMessage(code, error, self.icon)

    def addProgramRule(self):
        name = self.lineEditNameProgram.text()
        # Check if the name is'nt empty
        if name != '':
            description = self.textEditDescriptionProgram.toPlainText()
            direction = 'in' if self.comboBoxDirectionProgram.currentText() == 'Dentro' else 'out'
            enable = 'yes' if self.checkBoxEnableProgram.isChecked() else 'no'
            action = 'allow' if self.comboBoxActionProgram.currentText() == 'Permitir' else 'block'
            selectedProgram = None if self.comboBoxProgram.currentText() == 'Todos' else self.lineEditProgram.text()
            protocol = None
            self.rulesConnection.addRule(name, direction, action, protocol, description, enable, program=selectedProgram)
        else:
            code = 'No ingresó el nombre de la regla'
            error = 'Debe ingresar el nombre de la regla.\nRevise la ayuda para crear nuevas reglas'
            self.message.showMessage(code, error, self.icon)

    def addIpRule(self):
        pass

    def setUpFilledWindow(self, protocol):
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
            self.lineEditName.setText(self.getRule[0]['Nombre de regla'])
            self.comboBoxDirection.setCurrentText(self.getRule[0]['Dirección'])
            self.comboBoxAction.setCurrentText(self.getRule[0]['Acción'])
            self.comboBoxProtocol.setCurrentText(protocol)

            if 'Descripción' in self.getRule[0]:
                self.textEditDescription.setText(self.getRule[0]['Descripción'])
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
            return True
        except Exception as exception:
            code = 'No se pudo acceder a la regla seleccionada'
            self.message.showMessage(code, exception, self.icon)
            return False








    # Method to delete the selected rule
    def deleteSelectedRule(self):
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
                self.message.showMessage(code, exception, self.icon)

    # Edit the selected rule
    def editSelectedRule(self):
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
            self.message.showMessage(code, error, self.icon)

    def getSelectedRule(self, row):
        newForm = QtWidgets.QDialog()
        translations = {
        "Pública": "public",
        "Privada": "private",
        "Dominio": "domain",
        }
        name = self.newTable.item(row, 0).text()
        profile = self.newTable.item(row,2).text()
        direction = self.newTable.item(row,4).text()
        protocol = self.newTable.item(row,5).text()
        
        direction = 'in' if direction == 'Dentro' else 'out'

        values = profile.split(",")
        translated_values = [translations[value.strip()] if value.strip() in translations else value.strip() for value in values]
        translated_value = ",".join(translated_values)
        profile = translated_value

        search = self.rulesConnection.searchRules(name, profile, direction)
        self.initRuleWindow(newForm, protocol, search, True)