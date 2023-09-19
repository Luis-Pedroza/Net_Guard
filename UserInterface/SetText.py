from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from Controller.Language import LanguageManager, ErrorLanguage

class SetCurrentText():
    '''
    A class for setting the current text of various UI elements based on the selected language.

    Attributes:
        language (LanguageManager): Manages language settings and interactions with the database.
        translator (QtCore.QTranslator): Handles translation of text to the selected language.

    Methods:
        __init__(self)
            Initializes the SetCurrentText class. It sets up the language manager and translator.

        execute_translator(self)
            Configures the translator based on the current language setting.

        set_about(self, about_object, main_window)
            Sets the text of UI elements related to the About window.

        set_alerts(self, alerts_object)
            Sets the text of UI elements related to alerts and notifications.

        set_ports_tab(self, ports_object, main_window)
            Sets the text of UI elements in the Ports Tab.

        set_scan_tab(self, scan_object, main_window)
            Sets the text of UI elements in the Scan Ports Tab.

        set_rules_table(self, rules_object, main_window)
            Sets the text of UI elements in the Rules Tab.

        set_rules_window(self, rules_object, main_window)
            Sets the text of UI elements in the Rules Window.

        set_main_window(self, main_object, main_window)
            Sets the text of UI elements in the main window.

    '''
    def __init__(self):
        self.language = LanguageManager()
        self.translator = QtCore.QTranslator()

    def execute_translator(self):
        '''
        Configures the translator based on the current language setting.

        Args:
            None

        Returns:
            None

        Example Usage:
            current_texts = SetCurrentText()
            current_texts.execute_translator()

        '''
        self._translate = QtCore.QCoreApplication.translate
        self.mainMessage = QMessageBox()
        self.mainMessage.setIcon(QMessageBox.Critical)
        self.mainMessage.setStandardButtons(QMessageBox.Ok)
        self.mainMessage.setWindowIcon(QIcon("Resources/icon.ico"))
        self.mainMessage.setWindowTitle('ERROR')
        try: 
            self.current_language = self.language.get_language()
            if hasattr(self, 'translator'):
                QtCore.QCoreApplication.removeTranslator(self.translator)

            if self.current_language != 'en' and hasattr(self, 'translator'):
                QtCore.QCoreApplication.removeTranslator(self.translator)
                self.translator = QtCore.QTranslator()
                self.translator.load(f"Resources/lan/language_{self.current_language}.qm")
                QtCore.QCoreApplication.installTranslator(self.translator)
        except ErrorLanguage as exception:
            error_code = exception.error_code
            error_description = str(exception)
            self.mainMessage.setText(error_code)
            self.mainMessage.setInformativeText(str(error_description))
            self.mainMessage.exec_()
        except Exception as exception:
            error_description = str(exception)
            self.mainMessage.setText('ERROR_SetCurrentText_Translator')
            self.mainMessage.setInformativeText(str(exception))
            self.mainMessage.exec_()

    def set_about(self, about_object, main_window):
        '''
        Sets the text of UI elements related to the About window.

        Args:
            about_object: The About window object.
            main_window: The main window object.

        Returns:
            None

        Example Usage:
            current_texts = SetCurrentText()
            current_texts.set_about(about_window, main_window)

        '''
        self.execute_translator()
        main_window.setWindowTitle(self._translate("AboutWindow", "Net Guard"))

        about_text = self._translate("AboutWindow", '''
Net Guard is a Python-based desktop application.

It allows users to visualize and manage connections made through TCP and UDP ports.
It offers features such as port scanning, dynamic port range modification, firewall rule control, and detailed information display about established connections, additionally, a database is implemented to store ports information. 

The main objective of NetGuard is to provide users with increased control and security over their network, enabling them to make informed decisions regarding incoming and outgoing connections on their computer.

The Net Guard application is a comprehensive network management tool designed to provide users with control and information about their network settings and activity.

For more, visit:

        ''')
        about_object.about_text.setPlainText(self._translate("AboutWindow", about_text))
        about_object.close_window.setText(self._translate("AboutWindow", "Ok"))

    def set_alerts(self, alerts_object):
        '''
        Sets the text of UI elements related to alerts and notifications.

        Args:
            alerts_object: The alerts object.

        Returns:
            None

        Example Usage:
            current_texts = SetCurrentText()
            current_texts.set_alerts(alerts_object)

        '''
        self.execute_translator()
        alerts_object.mainMessage.setWindowTitle(self._translate('Alerts', 'Notice'))

    def set_ports_tab(self, ports_object, main_window):
        '''
        Sets the text of UI elements in the Ports Tab.

        Args:
            ports_object: The Ports Tab object.
            main_window: The main window object.

        Returns:
            None

        Example Usage:
            current_texts = SetCurrentText()
            current_texts.set_ports_tab(ports_object, main_window)

        '''
        self.execute_translator()
        main_window.setWindowTitle(self._translate("PortsTab", 'Search'))

        item = ports_object.new_table.horizontalHeaderItem(0)
        item.setText(self._translate("PortsTab", "Port"))
        item = ports_object.new_table.horizontalHeaderItem(1)
        item.setText(self._translate("PortsTab", "Service"))
        item = ports_object.new_table.horizontalHeaderItem(2)
        item.setText(self._translate("PortsTab", "Protocol"))
        item = ports_object.new_table.horizontalHeaderItem(3)
        item.setText(self._translate("PortsTab", "Description"))
        item = ports_object.new_table.horizontalHeaderItem(4)
        item.setText(self._translate("PortsTab", "Reference"))

    def set_scan_tab(self, scan_object, main_window):
        '''
        Sets the text of UI elements in the Scan Ports Tab.

        Args:
            scan_object: The Scan Ports Tab object.
            main_window: The main window object.

        Returns:
            None

        Example Usage:
            current_texts = SetCurrentText()
            current_texts.set_scan_tab(scan_object, main_window)

        '''
        self.execute_translator()
        main_window.setWindowTitle(self._translate('ScanTab', "Ports Range"))
        scan_object.checkBox_TCP.setText(self._translate('ScanTab', "Change TCP range"))
        scan_object.checkBox_UDP.setText(self._translate('ScanTab', "Change UDP range"))
        scan_object.change_range_btn.setText(self._translate('ScanTab', "Change"))
        scan_object.reset_values_btn.setText(self._translate('ScanTab', "Reset"))
        scan_object.cancel_btn.setText(self._translate('ScanTab', "Cancel"))

        scan_object.rule_name_missing_message = self._translate("ScanTab", 'Selected range has been changed')
        scan_object.option_not_selected = self._translate("ScanTab", 'Must select an option')

    def set_rules_table(self, rules_object, main_window):
        '''
        Sets the text of UI elements in the Rules Tab.

        Args:
            rules_object: The Rules Tab object.
            main_window: The main window object.

        Returns:
            None

        Example Usage:
            current_texts = SetCurrentText()
            current_texts.set_rules_table(rules_object, main_window)

        '''
        self.execute_translator()
        main_window.setWindowTitle(self._translate("RulesTable", "Search"))

        item = rules_object.new_table.horizontalHeaderItem(0)
        item.setText(self._translate("RulesTable", "Rule"))
        item = rules_object.new_table.horizontalHeaderItem(1)
        item.setText(self._translate("RulesTable", "Enable"))
        item = rules_object.new_table.horizontalHeaderItem(2)
        item.setText(self._translate("RulesTable", "Profile"))
        item = rules_object.new_table.horizontalHeaderItem(3)
        item.setText(self._translate("RulesTable", "Action"))
        item = rules_object.new_table.horizontalHeaderItem(4)
        item.setText(self._translate("RulesTable", "Direction"))
        item = rules_object.new_table.horizontalHeaderItem(5)
        item.setText(self._translate("RulesTable", "Protocol"))

    def set_rules_window(self, rules_object, main_window):
        '''
        Sets the text of UI elements in the Rules Window.

        Args:
            rules_object: The Rules Window object.
            main_window: The main window object.

        Returns:
            None

        Example Usage:
            current_texts = SetCurrentText()
            current_texts.set_rules_window(rules_object, main_window)

        '''
        self.execute_translator()
        main_window.setWindowTitle(self._translate("RulesWindow", "Rule"))

        rules_object.label_name.setText(self._translate("RulesWindow", "Name"))
        rules_object.label_description.setText(self._translate("RulesWindow", "Description"))
        rules_object.checkBox_enable.setText(self._translate("RulesWindow", "Enable"))
        rules_object.label_direction.setText(self._translate("RulesWindow", "Direction"))
        rules_object.comboBox_direction.addItem(self._translate("RulesWindow", "Inbound"))
        rules_object.comboBox_direction.addItem(self._translate("RulesWindow", "Outbound"))
        rules_object.label_action.setText(self._translate("RulesWindow", "Action"))
        rules_object.comboBox_action.addItem(self._translate("RulesWindow", "Block"))
        rules_object.comboBox_action.addItem(self._translate("RulesWindow", "Allow"))
        rules_object.label_protocol.setText(self._translate("RulesWindow", "Protocol"))
        rules_object.comboBox_protocol.addItem(self._translate("RulesWindow", "Any"))
        rules_object.comboBox_protocol.addItem(self._translate("RulesWindow", "TCP"))
        rules_object.comboBox_protocol.addItem(self._translate("RulesWindow", "UDP"))
        rules_object.label_profile.setText(self._translate("RulesWindow", "Profile"))
        rules_object.comboBox_profile.addItem(self._translate("RulesWindow", "Current"))
        rules_object.comboBox_profile.addItem(self._translate("RulesWindow", "Domain"))
        rules_object.comboBox_profile.addItem(self._translate("RulesWindow", "Private"))
        rules_object.comboBox_profile.addItem(self._translate("RulesWindow", "Domain & Private"))
        rules_object.comboBox_profile.addItem(self._translate("RulesWindow", "Public"))
        rules_object.comboBox_profile.addItem(self._translate("RulesWindow", "Domain & Public"))
        rules_object.comboBox_profile.addItem(self._translate("RulesWindow", "Private & Public"))
        rules_object.comboBox_profile.addItem(self._translate("RulesWindow", "Any"))
        rules_object.label_port.setText(self._translate("RulesWindow", "Port"))
        rules_object.comboBox_port.addItem(self._translate("RulesWindow", "Any"))
        rules_object.comboBox_port.addItem(self._translate("RulesWindow", "Range"))
        rules_object.label_program.setText(self._translate("RulesWindow", "Program"))
        rules_object.comboBox_program.addItem(self._translate("RulesWindow", "Any"))
        rules_object.comboBox_program.addItem(self._translate("RulesWindow", "Select"))
        rules_object.label_IP.setText(self._translate("RulesWindow", "IP Direction"))
        rules_object.txt_add_btn = self._translate("RulesWindow", "Add")
        rules_object.txt_cancel_btn = self._translate("RulesWindow", "Cancel")
        rules_object.txt_edit_btn = self._translate("RulesWindow", "Edit")
        rules_object.txt_delete_btn = self._translate("RulesWindow", "Delete")
        rules_object.name_missing_error = 'Specify the name of the rule'
        rules_object.name_missing_description = 'To create a new rule you must specify at least the name of the rule.\nCheck help to create a new rule'
        rules_object.rule_unable = 'Unable to access the selected rule'
        rules_object.deleted_alert = 'The selected rules has been deleted'
        rules_object.rule_changed = 'The rule has been changed'
        rules_object.added_rule = 'The new rules has been added'


    def set_main_window(self, main_object, main_window):
        '''
        Sets the text of UI elements in the main window.

        Args:
            main_object: The main object.
            main_window: The main window object.

        Returns:
            None

        Example Usage:
            current_texts = SetCurrentText()
            current_texts.set_main_window(main_object, main_window)

        '''
        self.execute_translator()
        main_window.setWindowTitle(self._translate("MainWindow", "Net Guard"))

        # ************************************************************
        # ************************* TAB SCAN *************************
        # ************************************************************
        main_object.tabWidget.setTabText(main_object.tabWidget.indexOf(main_object.tab_Scan), self._translate("MainWindow", "Scan"))

        item = main_object.scan_table.horizontalHeaderItem(0)
        item.setText(self._translate("MainWindow", "Protocol"))
        item = main_object.scan_table.horizontalHeaderItem(1)
        item.setText(self._translate("MainWindow", "Local Address"))
        item = main_object.scan_table.horizontalHeaderItem(2)
        item.setText(self._translate("MainWindow", "Remote Address"))
        item = main_object.scan_table.horizontalHeaderItem(3)
        item.setText(self._translate("MainWindow", "State"))
        item = main_object.scan_table.horizontalHeaderItem(4)
        item.setText(self._translate("MainWindow", "PID"))
        item = main_object.scan_table.horizontalHeaderItem(5)
        item.setText(self._translate("MainWindow", "Program"))

        main_object.label_rangeTCP.setText(self._translate("MainWindow", "TCP Range:"))
        main_object.label_rangeUDP.setText(self._translate("MainWindow", "UDP Range:"))

        main_object.port_scan_btn.setText(self._translate("MainWindow", "Update"))
        main_object.edit_range_btn.setText(self._translate("MainWindow", "Modify"))

        # ************************************************************
        # ************************* TAB RULES ************************
        # ************************************************************
        main_object.tabWidget.setTabText(main_object.tabWidget.indexOf(main_object.tab_Rules), self._translate("MainWindow", "Rules"))

        main_object.label_rule.setText(self._translate("MainWindow", "Name"))
        main_object.label_profile.setText(self._translate("MainWindow", "Profile"))

        main_object.comboBox_rule_profile.clear()
        main_object.comboBox_rule_profile.addItem(self._translate("MainWindow", "Any"))
        main_object.comboBox_rule_profile.addItem(self._translate("MainWindow", "Domain"))
        main_object.comboBox_rule_profile.addItem(self._translate("MainWindow", "Private"))
        main_object.comboBox_rule_profile.addItem(self._translate("MainWindow", "Domain & Private"))
        main_object.comboBox_rule_profile.addItem(self._translate("MainWindow", "Public"))
        main_object.comboBox_rule_profile.addItem(self._translate("MainWindow", "Domain & Public"))
        main_object.comboBox_rule_profile.addItem(self._translate("MainWindow", "Private & Public"))

        main_object.label_direction.setText(self._translate("MainWindow", "Direction"))
        main_object.comboBox_rule_direction.clear()
        main_object.comboBox_rule_direction.addItem(self._translate("MainWindow", "Any"))
        main_object.comboBox_rule_direction.addItem(self._translate("MainWindow", "Inbound"))
        main_object.comboBox_rule_direction.addItem(self._translate("MainWindow", "Outbound"))
        main_object.search_rule_btn.setText(self._translate("MainWindow", "Search"))

        item = main_object.rules_table.horizontalHeaderItem(0)
        item.setText(self._translate("MainWindow", "Rule"))
        item = main_object.rules_table.horizontalHeaderItem(1)
        item.setText(self._translate("MainWindow", "Enable"))
        item = main_object.rules_table.horizontalHeaderItem(2)
        item.setText(self._translate("MainWindow", "Profile"))
        item = main_object.rules_table.horizontalHeaderItem(3)
        item.setText(self._translate("MainWindow", "Action"))
        item = main_object.rules_table.horizontalHeaderItem(4)
        item.setText(self._translate("MainWindow", "Direction"))
        item = main_object.rules_table.horizontalHeaderItem(5)
        item.setText(self._translate("MainWindow", "Protocol"))

        main_object.reload_rules_table.setText(self._translate("MainWindow", "Update"))
        main_object.new_rule_btn.setText(self._translate("MainWindow", "Add"))

        # ************************************************************
        # ************************* TAB PORTS ************************
        # ************************************************************
        main_object.tabWidget.setTabText(main_object.tabWidget.indexOf(main_object.tab_Ports), self._translate("MainWindow", "Ports"))

        main_object.search_port_btn.setText(self._translate("MainWindow", "Search"))
        main_object.label_port.setText(self._translate("MainWindow", "Port"))
        main_object.label_service.setText(self._translate("MainWindow", "Service"))
        main_object.label_protocol.setText(self._translate("MainWindow", "Protocol"))
        main_object.comboBox_protocol.clear()
        main_object.comboBox_protocol.addItem(self._translate("MainWindow", "Both"))
        main_object.comboBox_protocol.addItem(self._translate("MainWindow", "TCP"))
        main_object.comboBox_protocol.addItem(self._translate("MainWindow", "UDP"))

        item = main_object.ports_table.horizontalHeaderItem(0)
        item.setText(self._translate("MainWindow", "Port"))
        item = main_object.ports_table.horizontalHeaderItem(1)
        item.setText(self._translate("MainWindow", "Service"))
        item = main_object.ports_table.horizontalHeaderItem(2)
        item.setText(self._translate("MainWindow", "Protocol"))
        item = main_object.ports_table.horizontalHeaderItem(3)
        item.setText(self._translate("MainWindow", "Description"))
        item = main_object.ports_table.horizontalHeaderItem(4)
        item.setText(self._translate("MainWindow", "Reference"))

        main_object.previous_table_btn.setText(self._translate("MainWindow", "Back"))
        main_object.next_table_btn.setText(self._translate("MainWindow", "Next"))

        # *************************************************************"
        # ************************* MENU BAR **************************"
        # *************************************************************"
        main_object.file_menu.setTitle(self._translate("MainWindow", "File"))
        main_object.edit_menu.setTitle(self._translate("MainWindow", "Edit"))
        main_object.config_menu.setTitle(self._translate("MainWindow", "Configuration"))
        main_object.help_menu.setTitle(self._translate("MainWindow", "Help"))

        main_object.action_save_scan.setText(self._translate("MainWindow", "Save scan"))
        main_object.action_save_rules.setText(self._translate("MainWindow", "Save rules"))

        main_object.action_new_rule.setText(self._translate("MainWindow", "New rule"))
        main_object.action_change_range.setText(self._translate("MainWindow", "Change ports range"))
        main_object.action_reload_scan.setText(self._translate("MainWindow", "Update scan"))

        main_object.menu_select_language.setTitle(self._translate("MainWindow", "Language"))
        main_object.action_select_Spanish.setText(self._translate("MainWindow", "Spanish"))
        main_object.action_select_english.setText(self._translate("MainWindow", "English"))
        main_object.menu_select_theme.setTitle(self._translate("MainWindow", "Theme"))
        main_object.action_select_dark.setText(self._translate("MainWindow", "Dark"))
        main_object.action_select_light.setText(self._translate("MainWindow", "Light"))

        main_object.help_change_range.setText(self._translate("MainWindow", "Change ports range"))
        main_object.help_new_rule.setText(self._translate("MainWindow", "Add new rule"))
        main_object.help_change_rule.setText(self._translate("MainWindow", "Edit rule"))
        main_object.help_search_rule.setText(self._translate("MainWindow", "Search rule"))
        main_object.help_search_port.setText(self._translate("MainWindow", "Search port"))
        main_object.action_About.setText(self._translate("MainWindow", "About Net Guard"))

        # *************************************************************"
        # ************************* EXCEPTIONS **************************"
        # *************************************************************"
        main_object.rule_name_missing_message = self._translate("MainWindow", "Must specify the name of the rule")
        main_object.rule_name_missing_description = self._translate("MainWindow", "You must enter the name of the rule to be able to perform a search")

        main_object.no_matching_data_message = self._translate("MainWindow", "No matching data found")
        main_object.no_matching_data_description = self._translate("MainWindow", "The search did not return any data matching the parameters")

        main_object.unregistered_port_message = self._translate("MainWindow", "Unregistered port")
        main_object.unregistered_port_description = self._translate("MainWindow", "The port you are trying to search for is not registered by the IANA")

        main_object.invalid_search_message = self._translate("MainWindow", "Cannot perform search")
        main_object.invalid_search_description = self._translate("MainWindow", "The search cannot be processed as specified, please review the search help")

        main_object.port_not_found_message = self._translate("MainWindow", "No matching data found")
        main_object.port_not_found_description = self._translate("MainWindow", "The search did not return any data matching the parameters")









