# ***************************************************
# FILE: UI_Scan_Tab.py
#
# DESCRIPTION: 
# Initialize the window to change or reset the values of the range
#
# AUTHOR:  Luis Pedroza
# CREATED: 18/04/2023 (dd/mm/yy)
# ***************************************************

from PyQt5 import QtCore, QtWidgets, QtGui
from Controller_Module.Scan import ScanPorts
from UI_Module.UI_Message import PopUpMessage

class PortsRangeWindow(object):
    def __init__(self):
        super().__init__()
        self.range = ScanPorts()
        self.message=PopUpMessage()
        self.icon = QtWidgets.QMessageBox.Information

    def setUpWindow(self, MainWindow):
        # initialize the main window with the specifications
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(380, 250)
        MainWindow.setWindowTitle("Rango de Puertos")
        MainWindow.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))

        # initialize  the options
        self.checkTCP = QtWidgets.QCheckBox(MainWindow)
        self.checkTCP.setGeometry(QtCore.QRect(80, 50, 121, 17))
        self.checkTCP.setObjectName("checkTCP")
        self.checkTCP.setText("Cambiar rango TCP")
        self.rangeTCP = QtWidgets.QSpinBox(MainWindow)
        self.rangeTCP.setGeometry(QtCore.QRect(220, 50, 60, 22))
        self.rangeTCP.setObjectName("rangeTCP")
        self.rangeTCP.setMaximum(16384)
        self.rangeTCP.setMinimum(255)

        self.checkUDP = QtWidgets.QCheckBox(MainWindow)
        self.checkUDP.setGeometry(QtCore.QRect(80, 95, 121, 17))
        self.checkUDP.setObjectName("checkUDP")
        self.checkUDP.setText("Cambiar rango UDP")
        self.rangeUDP = QtWidgets.QSpinBox(MainWindow)
        self.rangeUDP.setGeometry(QtCore.QRect(220, 90, 60, 22))
        self.rangeUDP.setObjectName("rangeUDP")
        self.rangeUDP.setMaximum(16384)
        self.rangeUDP.setMinimum(255)
        
        # Button to change the range
        self.changeRangeBtn = QtWidgets.QToolButton(MainWindow)
        self.changeRangeBtn.setGeometry(QtCore.QRect(20, 200, 101, 26))
        self.changeRangeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.changeRangeBtn.setObjectName("changeRangeBtn")
        self.changeRangeBtn.setText("Cambiar")
        self.changeRangeBtn.clicked.connect(lambda: self.change())
        self.changeRangeBtn.clicked.connect(MainWindow.close)

        # Button to reset the values
        # IANA recommendation 16384 ports
        self.resetValuesBtn = QtWidgets.QToolButton(MainWindow)
        self.resetValuesBtn.setGeometry(QtCore.QRect(140, 200, 101, 26))
        self.resetValuesBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.resetValuesBtn.setObjectName("resetValuesBtn")
        self.resetValuesBtn.setText("Restablecer")
        self.resetValuesBtn.clicked.connect(lambda: self.reset())
        self.resetValuesBtn.clicked.connect(MainWindow.close)

        # Button to close the window
        self.cancelBtn = QtWidgets.QToolButton(MainWindow)
        self.cancelBtn.setGeometry(QtCore.QRect(260, 200, 101, 26))
        self.cancelBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelBtn.setObjectName("cancelBtn")
        self.cancelBtn.setText("Cancelar")
        self.cancelBtn.clicked.connect(MainWindow.close)

    # Method to change range values
    def change(self):
        code = 'Se cambió el rango seleccionado'
        # change both values (TCP, UDP)
        # status False means an error
        if self.checkTCP.isChecked() and self.checkUDP.isChecked():
            statusTCP = self.range.change_ports_range('tcp', self.rangeTCP.value())
            statusUDP = self.range.change_ports_range('udp', self.rangeUDP.value())
            if statusTCP != False or statusUDP != False:
                self.message.show_message(code,'',self.icon)
        # change UDP
        elif self.checkUDP.isChecked():
            statusUDP = self.range.change_ports_range('udp', self.rangeUDP.value())
            if statusUDP != False:
                self.message.show_message(code,'',self.icon)
        # change TCP
        elif self.checkTCP.isChecked():
            statusTCP = self.range.change_ports_range('tcp', self.rangeTCP.value())
            if statusTCP != False:
                self.message.show_message(code,'',self.icon)
        # None checked
        else:
            code = 'No seleccionó una opción'
            self.message.show_message(code,'',self.icon)
            
    # method to reste default values
    def reset(self):
        code = 'Se restablecieron los valores predeterminados'
        # The recommended range is 16384
        statusTCP = self.range.change_ports_range('tcp',16384)
        statusUDP = self.range.change_ports_range('udp',16384)
        
        # Error control, status False means an error
        if statusTCP != False or statusUDP != False:
            self.message.show_message(code,'',self.icon)
        else: pass