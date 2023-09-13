# ***************************************************
# FILE: UI_Error.py
#
# DESCRIPTION:
# This module defines a class for displaying pop-up messages using the PyQt5 library.
# It provides a convenient way to show informative messages to the user with customizable icons.
#
# Classes:
#     PopUp_Messages
#
# Usage Example:
#     popup = PopUp_Messages()
#     popup.show_message("Error", "An unexpected error occurred.", QMessageBox.Critical)
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon


class PopUpMessage():
    """
    A class for displaying pop-up messages using the PyQt5 library.

    Attributes:
        None

    Methods:
        show_message(code, error, icon)
            Displays a pop-up message with the provided code, error message, and icon.

    Usage:
        popup = PopUpMessage()
        popup.show_message("Error", "An unexpected error occurred.", QMessageBox.Critical)

    """
    @staticmethod
    def show_message(code:str, error:str, icon:QMessageBox.Icon):
        """
        Display a pop-up message with the given code, error message, and icon.

        Args:
            code (str): The title or code for the message box.
            error (str): The informative text describing the error or message.
            icon (QMessageBox.Icon): The icon to be displayed in the message box.

        Returns:
            None

        """
        mainMessage = QMessageBox()
        mainMessage.setWindowTitle('Notice')
        mainMessage.setText(code)
        mainMessage.setInformativeText(str(error))
        mainMessage.setIcon(icon)
        mainMessage.setStandardButtons(QMessageBox.Ok)
        mainMessage.setWindowIcon(QIcon("Resources/icon.ico"))
        mainMessage.exec_()
