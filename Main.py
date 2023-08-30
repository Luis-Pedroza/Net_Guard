# ***************************************************
# FILE: Main.py
#
# DESCRIPTION:
# Application Entry Point and Main Window Initialization
#
# This script serves as the entry point for the application
# and initializes the main application window using PyQt5.
# The 'MainWindow' class is defined,
# which inherits from 'QtWidgets.QMainWindow'
# and 'Ui_MainWindow',
# enabling the integration of the UI design from the 'UI_Module'.
# The script creates an instance of the 'MainWindow' class,
# displays the main window, and starts the event loop for the application.
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ******************* ********************************

# Command to create the package
# pyinstaller --onedir --noconsole \
# --icon=Resources\icon.ico --uac-admin \
#     --add-data "Resources;Resources" -n "Net Guard" Main.py


import sys
from PyQt5 import QtWidgets
from UI_Module.MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Main application window class.

    This class initializes the main application window
    using the Ui_MainWindow class from UI_Module.
    It creates an instance of the QMainWindow and sets up the user interface.

    Attributes:
        ui (Ui_MainWindow): An instance of the Ui_MainWindow class
        for setting up the user interface.

    Methods:
        __init__(self)
            Initializes the MainWindow class and sets up the user interface.

    """

    def __init__(self):
        """
        Initializes the MainWindow class and sets up the user interface.
        """
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


# Initialize de mainWindow until program is closed
if __name__ == '__main__':
    """
    Application entry point.
    """
    InitMainWindow = QtWidgets.QApplication([])
    MainApp = MainWindow()
    MainApp.show()
    sys.exit(InitMainWindow.exec())
