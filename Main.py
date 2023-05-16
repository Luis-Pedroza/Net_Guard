# ***************************************************
# FILE: Main.py
#
# DESCRIPTION: 
# This code imports the main UI and initialize it
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ******************* ********************************

# Command to create an exe.
# pyinstaller --onedir --noconsole --icon=Resources\icon.ico --uac-admin --add-data "Resources;Resources" -n "Net Guard" Main.py


import sys
from PyQt5 import QtWidgets
from UI_Module.MainWindow import Ui_MainWindow

#Initialize the Ui_MainWindow as a QMainWindow type
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

#Initialize de mainWindow until program is closed
if __name__ == '__main__':

    InitMainWindow = QtWidgets.QApplication([])    
    MainApp = MainWindow()
    MainApp.show()
    sys.exit(InitMainWindow.exec())