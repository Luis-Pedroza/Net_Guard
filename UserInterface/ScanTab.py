# ***************************************************
# FILE: UI_Scan_Tab.py
#
# DESCRIPTION:
#
# The PortsRangeWindow class is used for configuring and changing
# port ranges for TCP and UDP connections.
# It provides methods for changing the ranges,
# resetting them to defaults, and setting up the user interface for this purpose.
#
# AUTHOR:  Luis Pedroza
# CREATED: 18/04/2023 (dd/mm/yy)
# ***************************************************

from PyQt5 import QtCore, QtWidgets, QtGui
from Controller.Scan import ScanPorts
from .Alerts import PopUpMessage
from .SetText import SetCurrentText
from .Styles import SetCurrentTheme


class PortsRangeWindow(object):
    '''
    A class for configuring and changing port ranges for TCP and UDP connections.

    Attributes:
        range (ScanPorts): An object for scanning and changing port ranges.
        message (PopUpMessage): A class for displaying messages.
        icon (QtWidgets.QMessageBox.Icon): An icon for message boxes.

    Methods:
        __init__(self)
            Initializes the PortsRangeWindow class.

        setUp_window(self, main_window)
            Sets up the main window for changing port ranges.

        change_range(self)
            Changes the port ranges for TCP and/or UDP connections based on user input.

        reset_default_values(self)
            Resets the port ranges to default values.

    '''
    def __init__(self):
        super().__init__()
        self.current_text = SetCurrentText()
        self.current_theme = SetCurrentTheme()
        self.range = ScanPorts()
        self.message = PopUpMessage()
        self.icon = QtWidgets.QMessageBox.Information

    def setUp_window(self, main_window: QtWidgets.QMainWindow):
        '''
        Sets up the main window for changing port ranges.

        Args:
            main_window (QtWidgets.QMainWindow): The main window for configuring port ranges.

        Returns:
            None

        Raises:
            None

        Example Usage:
            ports_range_window = PortsRangeWindow()
            ports_range_window.setUp_window(main_window)

        '''
        main_window.setObjectName("main_window")
        main_window.setFixedSize(380, 250)
        main_window.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))

        self.checkBox_TCP = QtWidgets.QCheckBox(main_window)
        self.checkBox_TCP.setGeometry(QtCore.QRect(80, 50, 121, 17))
        self.checkBox_TCP.setObjectName("checkBox_TCP")
        self.rangeTCP = QtWidgets.QSpinBox(main_window)
        self.rangeTCP.setGeometry(QtCore.QRect(220, 50, 60, 22))
        self.rangeTCP.setObjectName("rangeTCP")
        self.rangeTCP.setMaximum(16384)
        self.rangeTCP.setMinimum(255)

        self.checkBox_UDP = QtWidgets.QCheckBox(main_window)
        self.checkBox_UDP.setGeometry(QtCore.QRect(80, 95, 121, 17))
        self.checkBox_UDP.setObjectName("checkBox_UDP")
        self.rangeUDP = QtWidgets.QSpinBox(main_window)
        self.rangeUDP.setGeometry(QtCore.QRect(220, 90, 60, 22))
        self.rangeUDP.setObjectName("rangeUDP")
        self.rangeUDP.setMaximum(16384)
        self.rangeUDP.setMinimum(255)

        self.change_range_btn = QtWidgets.QToolButton(main_window)
        self.change_range_btn.setGeometry(QtCore.QRect(20, 200, 101, 26))
        self.change_range_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.change_range_btn.setObjectName("change_range_btn")
        self.change_range_btn.clicked.connect(lambda: self.change_range())
        self.change_range_btn.clicked.connect(main_window.close)

        # IANA recommendation 16384 ports
        self.reset_values_btn = QtWidgets.QToolButton(main_window)
        self.reset_values_btn.setGeometry(QtCore.QRect(140, 200, 101, 26))
        self.reset_values_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reset_values_btn.setObjectName("reset_values_btn")
        self.reset_values_btn.clicked.connect(lambda: self.reset_default_values())
        self.reset_values_btn.clicked.connect(main_window.close)

        self.cancel_btn = QtWidgets.QToolButton(main_window)
        self.cancel_btn.setGeometry(QtCore.QRect(260, 200, 101, 26))
        self.cancel_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(main_window.close)

        self.change_successful = ''
        self.option_not_selected = ''

        self.current_theme.set_selected_theme(main_window)
        self.current_text.set_scan_tab(self, main_window)

    def change_range(self):
        '''
        Changes the port ranges for TCP and/or UDP connections based on user input.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            ports_range_window = PortsRangeWindow()
            ports_range_window.change_range()

        '''
        # status False means an error
        if self.checkBox_TCP.isChecked() and self.checkBox_UDP.isChecked():
            statusTCP = self.range.change_ports_range('tcp', self.rangeTCP.value())
            statusUDP = self.range.change_ports_range('udp', self.rangeUDP.value())
            if statusTCP is not False or statusUDP is not False:
                self.message.show_message(self.change_successful, '', self.icon)
        elif self.checkBox_UDP.isChecked():
            statusUDP = self.range.change_ports_range('udp', self.rangeUDP.value())
            if statusUDP is not False:
                self.message.show_message(self.change_successful, '', self.icon)
        elif self.checkBox_TCP.isChecked():
            statusTCP = self.range.change_ports_range('tcp', self.rangeTCP.value())
            if statusTCP is not False:
                self.message.show_message(self.change_successful, '', self.icon)
        else:
            self.message.show_message(self.option_not_selected, '', self.icon)

    def reset_default_values(self):
        '''
        Resets the port ranges to default values.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Example Usage:
            ports_range_window = PortsRangeWindow()
            ports_range_window.reset()

        '''
        code = 'Defaults values were reset'
        # The recommended range is 16384
        statusTCP = self.range.change_ports_range('tcp', 16384)
        statusUDP = self.range.change_ports_range('udp', 16384)

        if statusTCP is not False or statusUDP is not False:
            self.message.show_message(code, '', self.icon)
        else: pass
