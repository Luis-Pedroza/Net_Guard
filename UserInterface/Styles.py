# ***************************************************
# FILE: name.py
#
# DESCRIPTION: 
# This allows user to change the theme on the UI
# It contains the dark_style specifications
# The SetCurrentTheme class allows to change between
# dark and default value (light)
#
# AUTHOR:  Luis Pedroza
# CREATED: 21/09/2023 (dd/mm/yyyy)
# ******************* ********************************

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from Controller.Configuration import ThemeManager, ErrorDataManager


class SetCurrentTheme():
    '''
    A class for setting the current theme of the main window.

    Methods:
        set_selected_theme(self, main_window):
            Sets the selected theme for the main window based on user preferences.

    '''
    def set_selected_theme(self, main_window):
        '''
        Sets the selected theme for the main window based on user preferences.

        Args:
            main_window: The main window of the application.

        Example Usage:
            theme_manager = SetCurrentTheme()
            main_window = QtWidgets.QMainWindow()
            theme_manager.set_selected_theme(main_window)

        '''
        self.theme = ThemeManager()
        self._translate = QtCore.QCoreApplication.translate
        self.mainMessage = QMessageBox()
        self.mainMessage.setIcon(QMessageBox.Critical)
        self.mainMessage.setStandardButtons(QMessageBox.Ok)
        self.mainMessage.setWindowIcon(QIcon("Resources/icon.ico"))
        self.mainMessage.setWindowTitle('ERROR')
        try:
            value = self.theme.get_theme()
            if value == 'dark':
                main_window.setStyleSheet(dark_style)
            else:
                main_window.setStyleSheet('')

        except ErrorDataManager as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.mainMessage.setText(error_code)
            self.mainMessage.setInformativeText(str(error_description))
            self.mainMessage.exec_()
        except Exception as exception:
            error_description = str(exception)
            self.mainMessage.setText('ERROR: UI_Styles_Theme')
            self.mainMessage.setInformativeText(str(exception))
            self.mainMessage.exec_()
dark_style = """
QMainWindow {
    background-color: #2E2E2E;
    color: #CCCCCC;
}

QDialog {
    background-color: #2E2E2E;
    color: #CCCCCC;
}

QTabWidget::pane {
    border: 1px solid #505050;
    background-color: #2E2E2E;
}

QTabBar::tab {
    padding: 5px 15px;
    background-color: #1E1E1E;
    color: #CCCCCC;
}

QTabBar::tab:selected {
    background-color: #404040;
}

QTableWidget {
    background-color: #2E2E2E;
    color: #CCCCCC;
    gridline-color: #505050;
}

QHeaderView::section {
    background-color: #1E1E1E; 
    color: #CCCCCC;
}

QComboBox {
    background-color: #1E1E1E;
    color: #CCCCCC;
    border: 1px solid #505050;
    padding: 3px;
    selection-background-color: #404040;
}

QComboBox QAbstractItemView {
    background-color: #1E1E1E;
    color: #CCCCCC;
}

QMenuBar {
    background-color: #1E1E1E;
    color: #CCCCCC;
}

QMenuBar::item {
    background-color: #1E1E1E;
    color: #CCCCCC;
}

QMenuBar::item:selected {
    background-color: #404040;
}
QMenuBar::item:hover {
    background-color: #1E1E1E;
}

QMenu {
    background-color: #1E1E1E;
    color: #CCCCCC;
}

QMenu::item {
    background-color: transparent;
    color: #CCCCCC;
}
QMenu::item:hover {
    background-color: #1E1E1E;
}

QMessageBox {
    background-color: #222;
    color: #FFF;
    border: none;
}

QPushButton {
    background-color: #1E1E1E;
    color: #CCCCCC;
    border: 1px solid #505050;
    padding: 5px 15px;
}

QPushButton:hover {
    background-color: #404040;
}

QPushButton:pressed {
    background-color: #004C8F;
}

QToolButton {
    background-color: #1E1E1E;
    color: #CCCCCC;
    border: 1px solid #505050;
}

QToolButton:hover {
    background-color: #404040;
}

QToolButton:pressed {
    background-color: #004C8F;
}

QLineEdit, QTextEdit {
    background-color: #1E1E1E;
    color: #CCCCCC;
    border: 1px solid #505050;
    padding: 3px;
    selection-background-color: #404040;
}

QPlainTextEdit {
    background-color: #1E1E1E;
    color: #CCCCCC;
    border: none;
    border-radius: 5px;
    padding: 5px;
}

QPlainTextEdit QTextEdit {
    background-color: #1E1E1E;
    color: #CCCCCC;
    border: none;
}

QLabel {
    color: #CCCCCC;
}

QSpinBox {
    background-color: #1E1E1E;
    color: #CCCCCC;
    border: 1px solid #505050;
    padding: 3px;
    selection-background-color: #404040;
}

QCheckBox {
    color: #CCCCCC;
    border: none;
    spacing: 5px;
}
"""
