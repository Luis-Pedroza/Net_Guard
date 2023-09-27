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
from .SetText import SetCurrentText
from .Styles import SetCurrentTheme


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
    def show_message(self, code:str, error:str, icon:QMessageBox.Icon):
        """
        Display a pop-up message with the given code, error message, and icon.

        Args:
            code (str): The title or code for the message box.
            error (str): The informative text describing the error or message.
            icon (QMessageBox.Icon): The icon to be displayed in the message box.

        Returns:
            None

        """
        current_text = SetCurrentText()
        current_theme = SetCurrentTheme()
        self.mainMessage = QMessageBox()
        self.mainMessage.setText(code)
        self.mainMessage.setInformativeText(str(error))
        self.mainMessage.setIcon(icon)
        self.mainMessage.setStandardButtons(QMessageBox.Ok)
        self.mainMessage.setWindowIcon(QIcon("Resources/icon.ico"))
        current_text.set_alerts(self)
        current_theme.set_selected_theme(self.mainMessage)
        self.mainMessage.exec_()
