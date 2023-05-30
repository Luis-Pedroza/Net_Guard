
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

        #initialize a new widget and a layout
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.layOut = QtWidgets.QVBoxLayout(self.centralWidget)

        # get the data 
        dataList = self.rulesConnection.searchRules(self.name, self.profile, self.direction)

        # check if data has information
        if dataList:
            self.Form = QtWidgets.QWidget()
            self.newTable = QtWidgets.QTableWidget(self.centralWidget)
            header = ['Regla', 'Habilitada', 'Perfil', 'Acción', 'Dirección', 'Protocolo' ]
            self.newTable.setColumnCount(6)
            self.newTable.setRowCount(len(dataList))
            self.newTable.setHorizontalHeaderLabels(header)
            self.newTable.setGeometry(QtCore.QRect(1, 0, 759, 511))
            self.newTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.newTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            self.newTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            self.newTable.cellDoubleClicked.connect(lambda item: self.initRuleWindow(self.Form, self.newTable.item(item, 5).text(), dataList, True,))
            # REVISAR BUG AL ELIMINAR UNA REGLA Y QUERER ELIMINAR OTRA

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

                #add the table to the layout    
                self.layOut.addWidget(self.newTable)
                self.scrollArea = QtWidgets.QScrollArea()
                self.scrollArea.setWidgetResizable(True)
                self.scrollArea.setWidget(self.centralWidget)
                # set the scroll Area on the MainWindow
                MainWindow.setCentralWidget(self.scrollArea)

        # if there is'n data, initialize an empty table
        else: self.newTable = QtWidgets.QTableWidget(self.centralWidget)

    def initRuleWindow(self, Form, protocol=None, rule=None, action=False):
        Form.setObjectName("Form")
        Form.setWindowTitle("Regla")
        Form.setFixedSize(400, 476)
        Form.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))

        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 401, 471))
        self.tabWidget.setObjectName("tabWidget")

        self.tabPort = QtWidgets.QWidget()
        self.tabPort.setObjectName("tabPort")

        self.labelName = QtWidgets.QLabel(self.tabPort)
        self.labelName.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.labelName.setObjectName("labelName")
        self.labelName.setText("Nombre")
        self.lineEditName = QtWidgets.QLineEdit(self.tabPort)
        self.lineEditName.setGeometry(QtCore.QRect(70, 20, 291, 20))
        self.lineEditName.setObjectName("lineEditName")

        self.labelDescription = QtWidgets.QLabel(self.tabPort)
        self.labelDescription.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.labelDescription.setObjectName("labelDescription")
        self.labelDescription.setText("Descripción")
        self.textEditDescription = QtWidgets.QTextEdit(self.tabPort)
        self.textEditDescription.setGeometry(QtCore.QRect(20, 70, 341, 71))
        self.textEditDescription.setObjectName("textEditDescription")
        
        self.checkBoxEnable = QtWidgets.QCheckBox(self.tabPort)
        self.checkBoxEnable.setGeometry(QtCore.QRect(30, 160, 70, 17))
        self.checkBoxEnable.setObjectName("checkBoxEnable")
        self.checkBoxEnable.setText("Habilitada")

        self.labelDirection = QtWidgets.QLabel(self.tabPort)
        self.labelDirection.setGeometry(QtCore.QRect(30, 200, 61, 16))
        self.labelDirection.setObjectName("labelDirection")
        self.labelDirection.setText("Dirección")
        self.comboBoxDirection = QtWidgets.QComboBox(self.tabPort)
        self.comboBoxDirection.setGeometry(QtCore.QRect(80, 200, 69, 22))
        self.comboBoxDirection.setObjectName("comboBoxDirection")
        self.comboBoxDirection.addItem("Dentro")
        self.comboBoxDirection.addItem("Fuera")

        self.labelAction = QtWidgets.QLabel(self.tabPort)
        self.labelAction.setGeometry(QtCore.QRect(30, 244, 47, 13))
        self.labelAction.setObjectName("labelAction")
        self.labelAction.setText("Acción")
        self.comboBoxAction = QtWidgets.QComboBox(self.tabPort)
        self.comboBoxAction.setGeometry(QtCore.QRect(80, 240, 110, 22))
        self.comboBoxAction.setObjectName("comboBoxAction")
        self.comboBoxAction.addItem("Bloquear")
        self.comboBoxAction.addItem("Permitir")

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
        self.comboBoxPort.currentTextChanged.connect(self.selectedPort)
        self.lineEditPort = QtWidgets.QLineEdit(self.tabPort)
        self.lineEditPort.setGeometry(QtCore.QRect(210, 290, 151, 20))
        self.lineEditPort.setObjectName("lineEditPort")
        self.selectedPort(self.comboBoxPort.currentText())
        
        self.btnEdit = QtWidgets.QPushButton(self.tabPort)
        self.btnEdit.setGeometry(QtCore.QRect(70, 400, 101, 26))
        self.btnEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnEdit.setObjectName("btnEdit")
        self.btnEdit.setText("Editar")
        self.btnDelete = QtWidgets.QPushButton(self.tabPort)
        self.btnDelete.setGeometry(QtCore.QRect(250, 400, 101, 26))
        self.btnDelete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnDelete.setObjectName("btnDelete")
        self.btnDelete.setText("Eliminar")
        self.getRule  = rule
        # Two types of initialization 
        # If action == True, the windows is for edit and delete the rule
        if action == True:
            try:
                self.lineEditName.setText(rule[0]['Nombre de regla'])
                self.textEditDescription.setText(rule[0]['Descripción'])
                self.comboBoxDirection.setCurrentText(rule[0]['Dirección'])
                self.comboBoxAction.setCurrentText(rule[0]['Acción'])
                self.comboBoxProtocol.setCurrentText(protocol)

                if 'LocalPort' in rule[0] or 'RemotePort' in rule[0]:
                    if rule[0]['LocalPort'] != 'Cualquiera':
                        self.comboBoxPort.setCurrentText('Rango')
                        self.lineEditPort.setText(rule[0]['LocalPort'])
                    elif rule[0]['RemotePort'] != 'Cualquiera':
                        self.comboBoxPort.setCurrentText('Rango')
                        self.lineEditPort.setText(rule[0]['RemotePort'])
                    else:
                        self.comboBoxPort.setCurrentText('Todos')
                else: 
                    self.comboBoxPort.setCurrentText('Todos')
                    self.comboBoxProtocol.addItem(rule[0]['Protocolo'])
                    self.comboBoxProtocol.setCurrentText(rule[0]['Protocolo'])
                    self.comboBoxProtocol.setEnabled(False)
                    self.comboBoxPort.setEnabled(False)
                    self.lineEditPort.setEnabled(False)

                if rule[0]['Habilitada'] == 'Sí':
                    self.checkBoxEnable.setChecked(True)

                valueProfile = rule[0]['Perfiles'].split(',')
                for profile in valueProfile:
                    if profile == "Pública":
                        self.checkBoxPublic.setChecked(True)
                    elif profile == "Privada":
                        self.checkBoxPrivate.setChecked(True)
                    elif profile == "Dominio":
                        self.checkBoxDomain.setChecked(True)

                self.btnEdit.setText("Editar")
                self.btnEdit.clicked.connect(self.editSelectedRule)
                self.btnEdit.clicked.connect(Form.close)
                self.btnDelete.setText("Eliminar")
                self.btnDelete.clicked.connect(self.deleteSelectedRule)
                self.btnDelete.clicked.connect(Form.close)
                Form.show()
            except Exception as exception:
                code = 'No se pudo acceder a la regla seleccionada'
                self.message.showMessage(code, exception, self.icon)
        # If action == False, the windows is for adding a rule
        else: 
            self.btnEdit.setText("Agregar")
            self.btnEdit.clicked.connect(self.addNewRule)
            self.btnEdit.clicked.connect(Form.close)
            self.btnDelete.setText("Cancelar")
            self.btnDelete.clicked.connect(Form.close)
            Form.show()

        self.tabWidget.addTab(self.tabPort, "Puerto")
        # self.tab_2 = QtWidgets.QWidget()
        # self.tab_2.setObjectName("tab_2")
        # self.tabWidget.addTab(self.tab_2, "Programa")
        # self.tab_5 = QtWidgets.QWidget()
        # self.tab_5.setObjectName("tab_5")
        # self.tabWidget.addTab(self.tab_5, "IP")
        
    # Method to alow or block the lineEditPort
    def selectedPort(self, text):
        if text == 'Todos':
            self.lineEditPort.setEnabled(False)
        else:
            self.lineEditPort.setEnabled(True)
    
    # Method to add a new rule
    def addNewRule(self):
        # NOTE: CHECK IF THE lineEditPort HAS AN ACCEPTABLE VALUE
        name = self.lineEditName.text()
        # Check if the name is'nt empty
        if name != '':
            description = self.textEditDescription.toPlainText()
            protocol = self.comboBoxProtocol.currentText()
            selectedPort = self.comboBoxPort.currentText()
            direction = 'in' if self.comboBoxDirection.currentText() == 'Dentro' else 'out'
            enable = 'yes' if self.checkBoxEnable.isChecked() else 'no'
            action = 'allow' if self.comboBoxAction.currentText() == 'Permitir' else \
            'block' if self.comboBoxAction.currentText() == 'Bloquear' else ''
            profile = ','.join([profile for profile, check_box in {'private': self.checkBoxPrivate, 'public': self.checkBoxPublic, 'domain': self.checkBoxDomain}.items() if check_box.isChecked()]) or 'any'
            # check the direction and select the port
            if direction == 'in':
                if selectedPort == 'Todos':
                    port = 'localport=any'
                else:
                    port = f'localport={self.lineEditPort.text()}'
            elif direction == 'out':
                if selectedPort == 'Todos':
                    port = 'remoteport=any'
                else:
                    port = f'remoteport={self.lineEditPort.text()}'
            self.rulesConnection.addRule(name, direction, action, protocol, port, profile, description, enable)
        # exception if name is empty
        else:
            code = 'No ingresó el nombre de la regla'
            error = 'Debe ingresar el nombre de la regla.\nRevise la ayuda para crear nuevas reglas'
            self.message.showMessage(code, error, self.icon)

    # Method to delete the selected rule
    def deleteSelectedRule(self):
        mainMessage = QtWidgets.QMessageBox()
        mainMessage.setWindowTitle('AVISO')
        mainMessage.setText('Se eliminara la regla seleccionada')
        mainMessage.setInformativeText('¿Desea continuar?')
        mainMessage.setIcon(QtWidgets.QMessageBox.Question)
        mainMessage.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        mainMessage.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        # translations of the profile
        translations = {
        "Pública": "public",
        "Privada": "private",
        "Dominio": "domain",
        }
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