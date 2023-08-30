# ***************************************************
# FILE: Main.py
#
# DESCRIPTION:
# This code imports the main UI and initialize it
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
