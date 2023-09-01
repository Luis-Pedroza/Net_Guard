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
from UI_Module.UI_Message import PopUpMessage

class Firewall_Rules():
    def __init__(self):
        self.message = PopUpMessage()
        self.iconFail = QMessageBox.Critical
        self.iconCorrect = QMessageBox.Information
        self.firewall = win32com.client.Dispatch("HNetCfg.FwPolicy2")

    # Method to add rule
    def addRule(self, name:str, description:str, enable:str, direction:str, action:str, protocol:str,  port:str, program:str, ip:str):
        new_rule = win32com.client.Dispatch("HNetCfg.FWRule")
        try:
            new_rule.Name = name
            new_rule.Description = 'None' if description == '' else description
            new_rule.Action = 1 if action == 'allow' else 0
            new_rule.Enabled = True if enable == 'yes' else False
            new_rule.Direction = 1 if direction == 'in' else 2

            if protocol == 'TCP':
                new_rule.Protocol = 6
            elif protocol == 'UDP':
                new_rule.Protocol = 17
            else:
                new_rule.Protocol = 256

            if port is not None and direction == 'in':
                new_rule.LocalPorts = port
            elif port is not None and direction == 'out':
                new_rule.RemotePorts = port
            
            if program is not None:
                new_rule.ApplicationName = program
            if ip is not None:
                new_rule.RemoteAddresses = ip

            self.firewall.Rules.Add(new_rule)
            self.message.show_message('Se agregó la regla','',self.iconCorrect)
        except Exception as exception:
            com_error_info = exception.excepinfo
            if com_error_info and len(com_error_info) > 5:
                error_code = com_error_info[5]
                error_message = win32api.FormatMessage(error_code)
                self.message.show_message('UNABLE_TO_EXECUTE_addRule', error_message, self.iconFail)
            else:
                self.message.show_message('UNABLE_TO_EXECUTE_addRule_1', exception.args[1], self.iconFail)



    # Method to get all the rules
    def showRules(self):
        rules = self.firewall.Rules
        firewall_rules = []
        try:
            for rule in rules:
                rule_info = {
                    "Name": rule.Name,
                    "Enabled": "Yes" if rule.Enabled else "No",
                    "Profiles": self.get_profiles(rule.Profiles),
                    "Action": "Allow" if rule.Action == 1 else "Block",
                    "Direction": "Inbound" if rule.Direction == 1 else "Outbound",
                    "Protocol": self.get_protocol_name(rule.Protocol),
                }
                firewall_rules.append(rule_info)
            return firewall_rules
        except Exception as exception: 
            self.message.show_message('UNABLE_TO_EXECUTE_showRules', exception, self.iconFail)

    # Method to search rules
    def searchRules(self, name: str, profile: str = None, direction: str = None):
        rules = self.firewall.Rules
        rules_list= []
        if direction == 'any': direction = None
        else: direction = 1 if direction == 'in' else 2
        profile = None if profile == 'any' else self.get_profiles(profile)
        try:
            for rule in rules:
                if rule.Name.lower() == name.lower() and \
                    (profile is None or rule.Profiles == profile) and \
                    (direction is None or rule.Direction == direction):
                    rules_list = self.get_searched_rule(rule, rules_list)
        except Exception as exception:
            self.message.show_message('UNABLE_TO_EXECUTE_searchRules', exception, self.iconFail)
        finally: return rules_list

    def get_protocol_name(self, protocol: str):
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
            return "Any"
        else:
            return protocol
        
    def get_profiles(self, profile):
        if isinstance(profile, str):
            profile = profile.lower()
            if profile == "domain":
                return 1
            elif profile == "private":
                return 2
            elif profile == "public":
                return 4

        elif isinstance(profile, int):
            profiles = []
            if profile & 1:
                profiles.append("Domain")
            if profile & 2:
                profiles.append("Private")
            if profile & 4:
                profiles.append("Public")
            return profiles
        
    def get_searched_rule(self, rule: win32com.client.CDispatch, rules_list: list) -> list:
        one_rule_list = []
        enable = 'Yes' if rule.Enabled == True else 'No'
        profile = self.get_profiles(rule.Profiles)
        profile = ', '.join(profile)
        action = 'Allow' if rule.Action == 1 else 'Block'
        direction = 'Inbound' if rule.Direction == 1 else 'Outbound'
        protocol = self.get_protocol_name(rule.Protocol)
        one_rule_list.append(rule.Name)
        one_rule_list.append(enable)
        one_rule_list.append(profile)
        one_rule_list.append(action)
        one_rule_list.append(direction)
        one_rule_list.append(protocol)
        rules_list.append(one_rule_list)
        return rules_list


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
                    self.message.show_message('UNABLE_To_deleteRule',output.stdout.splitlines()[1], self.iconFail)
                else: 
                    self.message.show_message('UNABLE_To_deleteRule',output.stdout, self.iconFail)
            else: 
                # Show confirmation
                self.message.show_message('Se eliminó la regla', '', self.iconCorrect)
        # exception control
        except subprocess.CalledProcessError as exception:
            self.message.show_message('UNABLE_TO_EXECUTE_deleteRule', exception, self.iconFail)

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
                    self.message.show_message('UNABLE_To_editRule',output.stdout.splitlines()[1], self.iconFail)
                else: 
                    self.message.show_message('UNABLE_To_editRule',output.stdout, self.iconFail)
            else: 
                # Show confirmation
                self.message.show_message('Se editó la regla','',self.iconCorrect)
        except subprocess.CalledProcessError as exception:
            # Exception control
            self.message.show_message('UNABLE_TO_EXECUTE_addRule', exception, self.iconFail)