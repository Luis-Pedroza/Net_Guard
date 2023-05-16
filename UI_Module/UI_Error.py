# ***************************************************
# FILE: UI_Error.py
#
# DESCRIPTION: 
# This code creates error or exception messages
# It receives: 
# Identifier of the message (code)
# exception or description of the message (error)
# icon for the window (icon)
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

class PopUp_Messages():
    @staticmethod
    def showMessage(code, error, icon):
        mainMessage = QMessageBox()
        mainMessage.setWindowTitle('AVISO')
        mainMessage.setText(code)
        mainMessage.setInformativeText(str(error))
        mainMessage.setIcon(icon)
        mainMessage.setStandardButtons(QMessageBox.Ok)
        mainMessage.setWindowIcon(QIcon("Resources/icon.ico"))
        mainMessage.exec_()