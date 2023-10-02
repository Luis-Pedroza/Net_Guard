# ***************************************************
# FILE: Main.py
#
# -*- coding: utf-8 -*-
# DESCRIPTION:
# This module defines a user interface using the PyQt5 library.
# It creates a dialog window with information about the Net Guard software.
#
# Form implementation generated from reading ui file 'About.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
#
# Classes:
#     Ui_Dialog
#
# Usage Example:
#     dialog_ui = Ui_Dialog()
#     dialog = QtWidgets.QDialog()
#     dialog_ui.setupUi(dialog)
#     dialog.exec_()
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ****************************************************

from PyQt5 import QtCore, QtWidgets, QtGui
from .Styles import SetCurrentTheme

class UiDialog(object):
    """
    A class for setting up the user interface of the Net Guard software information dialog.

    Attributes:
        None

    Methods:
        setupUi(Dialog)
            Sets up the UI elements of the dialog.
        retranslateUi(Dialog)
            Translates the UI elements to the desired language.

    """
    def setupUi(self, Dialog, current_text):
        """
        Set up the UI elements of the dialog.

        Args:
            Dialog (QtWidgets.QDialog): The dialog window to set up.

        Returns:
            None

        """
        self.current_text = current_text
        self.theme = SetCurrentTheme()
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 350)
        Dialog.setWindowIcon(QtGui.QIcon("Resources/icon.ico"))
        flags = Dialog.windowFlags()
        Dialog.setWindowFlags(flags & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.image_icon = QtWidgets.QLabel(Dialog)
        self.image_icon.setGeometry(QtCore.QRect(5, 0, 71, 71))
        self.image_icon.setObjectName("imageIcon")
        image = QtGui.QPixmap("Resources/icon.ico")
        self.image_icon.setPixmap(image.scaled(60, 60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

        self.about_text = QtWidgets.QPlainTextEdit(Dialog)
        self.about_text.setGeometry(QtCore.QRect(70, 0, 430, 400))
        self.about_text.setObjectName("plainTextEdit")
        self.about_text.setReadOnly(True)

        self.label_link = QtWidgets.QLabel(Dialog)
        self.label_link.setGeometry(QtCore.QRect(75, 260, 300, 20))
        self.label_link.setObjectName("label_link")
        self.label_link.setText('<a href="https://luis-pedroza.github.io/Net_Guard_Web/">luis-pedroza.github.io/Net_Guard_Web</a>')
        self.label_link.setOpenExternalLinks(True)

        self.close_window = QtWidgets.QPushButton(Dialog)
        self.close_window.setGeometry(QtCore.QRect(375, 290, 75, 23))
        self.close_window.setObjectName("closeWindow")
        self.close_window.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close_window.clicked.connect(Dialog.close)

        self.theme.set_selected_theme(Dialog)
        self.current_text.set_about(self, Dialog)
