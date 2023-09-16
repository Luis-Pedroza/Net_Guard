from PyQt5 import QtCore, QtWidgets, QtGui
from Controller.Language import LanguageManager

class SetCurrentText():
    def execute_translator(self):
        self.language = LanguageManager()
        current_language = self.language.get_language()
        if current_language != 'en':
            self.translator = QtCore.QTranslator()
            self.translator.load(f"test/language_{current_language}.qm")
            QtCore.QCoreApplication.installTranslator(self.translator)
        elif hasattr(self, 'translator'):
            QtCore.QCoreApplication.removeTranslator(self.translator)
        
        self._translate = QtCore.QCoreApplication.translate

    def set_alerts(self, alerts_object):
        self.execute_translator()
        alerts_object.mainMessage.setWindowTitle(self._translate('Alerts', 'Notice'))

    def set_ports_tab(self, ports_object, main_window):
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








