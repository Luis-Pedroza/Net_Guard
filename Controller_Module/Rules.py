# ***************************************************
# FILE: Rules.py
# -*- coding: utf-8 -*-
#
# DESCRIPTION: 
#
# AUTHOR:  Luis Pedroza
# CREATED: 11/04/2023 (dd/mm/yy)
# ***************************************************
import subprocess
import win32com.client
import win32api
from PyQt5.QtWidgets import QMessageBox
from UI_Module.UI_Error import PopUp_Messages

class Firewall_Rules():
    def __init__(self):
        self.message = PopUp_Messages()
        self.iconFail = QMessageBox.Critical
        self.iconCorrect = QMessageBox.Information
        self.firewall = win32com.client.Dispatch("HNetCfg.FwPolicy2")

    # Method to add rule
    def addRule(self, name:str, direction:str, action:str, protocol:str, port:str, profile:str, description:str, enable:str):
        new_rule = win32com.client.Dispatch("HNetCfg.FWRule")
        try:
            new_rule.Name = name
            new_rule.Description = 'None' if description == '' else description
            new_rule.Action = 1 if action == 'allow' else 0
            new_rule.Protocol = 6 if  protocol == 'TCP' else 17
            new_rule.Enabled = True if enable == 'yes' else False  # Habilitar la regla
            new_rule.Direction = 1 if direction == 'in' else 2
            if port == 'any':
                new_rule.LocalPorts = ''
                new_rule.RemotePorts = ''
            elif direction == 'in':
                new_rule.LocalPorts = port
            elif direction == "out":
                new_rule.RemotePorts = port

            self.firewall.Rules.Add(new_rule)
            self.message.showMessage('Se agregó la regla','',self.iconCorrect)
        except Exception as exception: 
            self.message.showMessage('UNABLE_TO_EXECUTE_addRule', exception, self.iconFail)
    # Method to get all the rules
    def showRules(self):
        rules = self.firewall.Rules
        firewall_rules = []
        try:
            for rule in rules:
                rule_info = {
                    "Name": rule.Name,
                    "Enabled": rule.Enabled,
                    "Profiles": self.get_profiles(rule.Profiles),
                    "Action": "Allow" if rule.Action == 1 else "Block",
                    "Direction": "Inbound" if rule.Direction == 1 else "Outbound",
                    "Protocol": self.get_protocol_name(rule.Protocol),
                }
                firewall_rules.append(rule_info)
            return firewall_rules
        except Exception as exception: 
            self.message.showMessage('UNABLE_TO_EXECUTE_showRules', exception, self.iconFail)

    def get_protocol_name(self, protocol):
        if protocol == 1:
            return "ICMP"
        elif protocol == 2:
            return "IGMP"
        elif protocol == 6:
            return "TCP"
        elif protocol == 17:
            return "UDP"
        elif protocol == 41:
            return "IPv6"
        elif protocol == 47:
            return "GRE"
        elif protocol == 58:
            return "ICMPv6"
        elif protocol == 256:
            return "ANY"
        else:
            return protocol
        
    def get_profiles(self, profile):
        profiles = []
        if profile & 1:
            profiles.append("Domain")
        if profile & 2:
            profiles.append("Private")
        if profile & 4:
            profiles.append("Public")
        return profiles

    # Method to search rules
    def searchRules(self, name, profile, direction):
        # check the direction, profile and initialize the command
        if direction == 'any' and profile == 'any':
            command = f'netsh advfirewall firewall show rule name="{name}" verbose'
        elif direction == 'any':
            command = f'netsh advfirewall firewall show rule name="{name}" profile="{profile}" verbose'
        elif profile == 'any':
            command = f'netsh advfirewall firewall show rule name="{name}" dir={direction} verbose'
        else:
            command = f'netsh advfirewall firewall show rule name="{name}" profile="{profile}" dir={direction} verbose'
        rule_data = []
        # Execute command and get output
        output = subprocess.run(command, shell=True, capture_output=True, encoding='cp850')
        lines = output.stdout.splitlines()
        # Check if rule is'nt showing because of the profile
        if lines[1] != 'Ninguna regla coincide con los criterios especificados.':
            try:
                rule_dict = {}
                for line in lines:
                    if line.startswith('Nombre de regla:'):
                        rule_dict = {'Nombre de regla': line.split(':', 1)[1].strip()}
                        rule_data.append(rule_dict)
                    elif rule_data and ':' in line:
                        key, value = [x.strip() for x in line.split(':', 1)]
                        rule_dict[key] = value
            # Exception control
            except Exception as exception:
                self.message.showMessage('UNABLE_TO_EXECUTE_searchRules', exception, self.iconFail)
            finally: return rule_data
        # if Therese's a problem with the profile, search without it  
        else:
            command = f'netsh advfirewall firewall show rule name="{name}" dir={direction} verbose'
            output = subprocess.run(command, shell=True, capture_output=True, encoding='cp850')
            lines = output.stdout.splitlines()
            try:
                rule_dict = {}
                for line in lines:
                    if line.startswith('Nombre de regla:'):
                        rule_dict = {'Nombre de regla': line.split(':', 1)[1].strip()}
                        rule_data.append(rule_dict)
                    elif rule_data and ':' in line:
                        key, value = [x.strip() for x in line.split(':', 1)]
                        rule_dict[key] = value
            # Exception control
            except Exception as exception:
                self.message.showMessage('UNABLE_TO_EXECUTE_searchRules', exception, self.iconFail)
            finally: return rule_data


    # Method to add rule
    def deleteRule(self, name, direction, profile, protocol, port):
        # check if rule has a port or a range of ports
        if port != None:
            command = f'netsh advfirewall firewall delete rule name= "{name}" dir={direction} profile = "{profile}" protocol={protocol} {port}'
        else:
            command = f'netsh advfirewall firewall delete rule name= "{name}" dir={direction} profile = "{profile}" protocol={protocol}'
        try:
            # Execute command and check if it has an error
            output = subprocess.run(command, shell=True, capture_output=True, encoding='cp850')
            if output.returncode != 0:
                # check if stdout has an error of use or elevation
                if output.stdout.splitlines()[1] != "":
                    self.message.showMessage('UNABLE_To_deleteRule',output.stdout.splitlines()[1], self.iconFail)
                else: 
                    self.message.showMessage('UNABLE_To_deleteRule',output.stdout, self.iconFail)
            else: 
                # Show confirmation
                self.message.showMessage('Se eliminó la regla', '', self.iconCorrect)
        # exception control
        except subprocess.CalledProcessError as exception:
            self.message.showMessage('UNABLE_TO_EXECUTE_deleteRule', exception, self.iconFail)

    # Method to edit rule
    def editRule(self, oldName, oldDirection,oldProtocol,name,direction, action, protocol, port, profile, description, enable):
        # Check if there is a description, if not then add None
        if description == "":
            description = "None"
        if protocol != 'any':
            command = f'netsh advfirewall firewall set rule name= "{oldName}" dir={oldDirection} protocol={oldProtocol} new name= "{name}" dir={direction} protocol={protocol} action={action} {port} profile={profile} description="{description}" enable={enable}'
        else:
            command = f'netsh advfirewall firewall set rule name= "{oldName}" dir={oldDirection} protocol={oldProtocol} new name= "{name}" dir={direction} protocol={protocol} action={action} profile={profile} description="{description}" enable={enable}'

        try:
            # Execute command and check if there's an error
            output = subprocess.run(command, shell=True, capture_output=True, encoding='cp850')
            if output.returncode != 0:
                if output.stdout.splitlines()[1] != "":
                    self.message.showMessage('UNABLE_To_editRule',output.stdout.splitlines()[1], self.iconFail)
                else: 
                    self.message.showMessage('UNABLE_To_editRule',output.stdout, self.iconFail)
            else: 
                # Show confirmation
                self.message.showMessage('Se editó la regla','',self.iconCorrect)
        except subprocess.CalledProcessError as exception:
            # Exception control
            self.message.showMessage('UNABLE_TO_EXECUTE_addRule', exception, self.iconFail)