# ***************************************************
# FILE: Rules.py
# -*- coding: utf-8 -*-
#
# DESCRIPTION:
# This class encapsulates the functionality for managing firewall rules.
#
# Classes:
#     Firewall_Rules
#
# Usage Example:
#     firewall_rules = Firewall_Rules()
#     firewall_rules.add_new_rule( /
#        "MyRule", "Allow incoming traffic", "yes", "in", "allow", "TCP", "80", "my_program.exe", "192.168.1.1")
#     rules_info = firewall_rules.get_all_rules()
#     matching_rules = firewall_rules.get_searched_rule("MyRule", profile="Domain", direction="in")
#     protocol_name = firewall_rules.get_protocol_name(6)
#     profile_value = firewall_rules.get_profiles("Private")
#     rules_list = firewall_rules.enlist_rules(rule, [])
#
#
# AUTHOR:  Luis Pedroza
# CREATED: 11/04/2023 (dd/mm/yy)
# ***************************************************

import win32com.client
import win32api
from PyQt5.QtWidgets import QMessageBox
from UI_Module.UI_Message import PopUpMessage


class Firewall_Rules():
    """
    A class for managing firewall rules.

    Attributes:
        message (PopUpMessage): An instance of PopUpMessage for displaying pop-up messages.
        iconFail (QMessageBox.Icon): An icon for displaying error messages.
        iconCorrect (QMessageBox.Icon): An icon for displaying success messages.
        firewall: An instance of the Windows Firewall policy.

    Methods:
        add_new_rule(name, description, enable, direction, action, protocol, port, program, ip)
            Adds a new firewall rule with the specified parameters.

    """
    def __init__(self):
        self.message = PopUpMessage()
        self.iconFail = QMessageBox.Critical
        self.iconCorrect = QMessageBox.Information
        self.firewall = win32com.client.Dispatch("HNetCfg.FwPolicy2")

    def add_new_rule(self, name: str, description: str, enable: bool, direction: str, action: str, protocol: str,  port: str, program: str, ip: str):
        """
        Adds a new firewall rule using the provided parameters.

        Args:
            name (str): The name of the firewall rule.
            description (str): The description of the firewall rule. If empty, it defaults to 'None'.
            enable (str): Whether the rule should be enabled ('yes') or disabled ('no').
            direction (str): The direction of the rule, 'in' for incoming or 'out' for outgoing traffic.
            action (str): The action to take for the rule, 'allow' or 'block'.
            protocol (str): The protocol of the rule, 'TCP', 'UDP', or any other value (defaulting to 'Other').
            port (str): The port to which the rule applies. If None, it does not specify a port.
            program (str): The name of the program/application associated with the rule. If None, it does not specify a program.
            ip (str): The IP address to which the rule applies. If None, it does not specify an IP address.

        Returns:
            None

        Raises:
            - Various exceptions if there is an issue while adding the rule.

        Example Usage:
            firewall_rules = Firewall_Rules()
            new_rule = firewall_rules.add_new_rule( \
            "MyRule", "Allow incoming traffic", "yes", "in", "allow", "TCP", "80", "my_program.exe", "192.168.1.1")

        """
        new_rule = win32com.client.Dispatch("HNetCfg.FWRule")
        try:
            new_rule.Name = name
            new_rule.Description = 'None' if description == '' else description
            new_rule.Action = 1 if action == 'Allow' else 0
            new_rule.Enabled = enable
            new_rule.Direction = 1 if direction == 'Inbound' else 2

            if protocol == 'TCP':
                new_rule.Protocol = 6
            elif protocol == 'UDP':
                new_rule.Protocol = 17
            else:
                new_rule.Protocol = 256
            # check value
            if port is not None and direction == 'Inbound':
                new_rule.LocalPorts = str(port)
            elif port is not None and direction == 'Outbound':
                new_rule.RemotePorts = str(port)
            # check value
            if program is not None:
                new_rule.ApplicationName = program
            # check value    
            if ip is not None:
                new_rule.RemoteAddresses = ip

            self.firewall.Rules.Add(new_rule)
            self.message.show_message('Se agregó la regla', '', self.iconCorrect)
        except Exception as exception:
            com_error_info = exception.excepinfo
            if com_error_info and len(com_error_info) > 5:
                error_code = com_error_info[5]
                error_message = win32api.FormatMessage(error_code)
                self.message.show_message('UNABLE_TO_EXECUTE_add_new_rule', error_message, self.iconFail)
            else:
                self.message.show_message('UNABLE_TO_EXECUTE_add_new_rule_1', exception.args[1], self.iconFail)

    def get_all_rules(self) -> list[dict]:
        """
        Retrieves and returns information about all the firewall rules.

        Returns:
            list: A list of dictionaries, where each dictionary represents a firewall rule with its attributes.
                Each dictionary contains the following keys:
                - "Name": The name of the firewall rule.
                - "Enabled": Whether the rule is enabled ("Yes") or disabled ("No").
                - "Profiles": The profiles to which the rule applies (e.g., "Domain, Private").
                - "Action": The action of the rule, either "Allow" or "Block".
                - "Direction": The direction of the rule, either "Inbound" or "Outbound".
                - "Protocol": The protocol used by the rule (e.g., "TCP", "UDP").

        Raises:
            - Various exceptions if there is an issue while retrieving rules.

        Example Usage:
            firewall_rules = Firewall_Rules()
            rules_info = firewall_rules.get_all_rules()
            for rule in rules_info:
                print(rule)

        """
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
            self.message.show_message('UNABLE_TO_EXECUTE_get_all_rules', exception, self.iconFail)

    def get_searched_rule(self, name: str, profile: str = None, direction: str = None) -> list[list]:
        """
        Searches for firewall rules based on the provided parameters and returns a list of matching rules.

        Args:
            name (str): The name of the firewall rule to search for.
            profile (str, optional): The profile to filter rules by (e.g., "Domain", "Private"). Default is None.
            direction (str, optional): The direction of the rule, either 'in' for inbound, 'out' for outbound, or 'any'. Default is None.

        Returns:
            list: A list of dictionaries, where each dictionary represents a matching firewall rule with its attributes.
                Each dictionary contains the following keys:
                - "Name": The name of the firewall rule.
                - "Enabled": Whether the rule is enabled ("Yes") or disabled ("No").
                - "Profiles": The profiles to which the rule applies (e.g., "Domain, Private").
                - "Action": The action of the rule, either "Allow" or "Block".
                - "Direction": The direction of the rule, either "Inbound" or "Outbound".
                - "Protocol": The protocol used by the rule (e.g., "TCP", "UDP").

        Raises:
            - Various exceptions if there is an issue while searching for rules.

        Example Usage:
            firewall_rules = Firewall_Rules()
            matching_rules = firewall_rules.get_searched_rule("MyRule", profile="Domain", direction="in")
            for rule in matching_rules:
                print(rule)

        """
        rules = self.firewall.Rules
        rules_list = []

        if direction == 'any':
            direction = None
        else:
            direction = 1 if direction == 'Inbound' else 2
        profile = None if self.get_profiles(profile) == 7 else self.get_profiles(profile)
        try:
            for rule in rules:
                if rule.Name.lower() == name.lower() and \
                    (profile is None or rule.Profiles == profile) and \
                        (direction is None or rule.Direction == direction):
                    rules_list = self.enlist_rules(rule, rules_list)
        except Exception as exception:
            self.message.show_message('UNABLE_TO_EXECUTE_get_searched_rule', exception, self.iconFail)
        finally:
            return rules_list

    def enlist_rules(self, rule: win32com.client.CDispatch, rules_list: list) -> list:
        """
        Extracts information from a firewall rule and appends it to a list of rules.

        Args:
            rule (win32com.client.CDispatch): The firewall rule from which to extract information.
            rules_list (list): The list of firewall rules to which the extracted information will be appended.

        Returns:
            list: The updated list of firewall rules with the extracted information.

        Example Usage:
            firewall_rules = Firewall_Rules()
            rule = <some_firewall_rule>  # Replace with an actual firewall rule object
            rules_list = firewall_rules.enlist_rules(rule, [])
            print(rules_list)  # Updated list of firewall rules

        """
        one_rule_list = []
        enable = 'Yes' if rule.Enabled == True else 'No'
        profile = self.get_profiles(rule.Profiles)
        profile = ', '.join(profile)
        action = 'Allow' if rule.Action == 1 else 'Block'
        direction = 'Inbound' if rule.Direction == 1 else 'Outbound'
        protocol = self.get_protocol_name(rule.Protocol)
        description = rule.Description
        local_port = rule.LocalPorts
        remote_Ports = rule.RemotePorts
        program = rule.ApplicationName
        ip = rule.RemoteAddresses

        one_rule_list.append(rule.Name)
        one_rule_list.append(enable)
        one_rule_list.append(profile)
        one_rule_list.append(action)
        one_rule_list.append(direction)
        one_rule_list.append(protocol)
        one_rule_list.append(description)
        one_rule_list.append(local_port)
        one_rule_list.append(remote_Ports)
        one_rule_list.append(program)
        one_rule_list.append(ip)
        rules_list.append(one_rule_list)
        return rules_list
    
    def edit_selected_rule(self, old_name: str, profile: str, old_direction, name: str, description: str, enable: bool, direction: str, action: str, protocol: str,  port: str, election_port: str, program: str, election_program: str, ip: str):
        # check exceptions of stupid users
        rules = self.firewall.Rules
        try:
            profile = None if self.get_profiles(profile) == 7 else self.get_profiles(profile)
            old_direction = 1 if old_direction == 'Inbound' else 2
            port = None if port == '' else port
            program = None if program == '' else program
            for rule in rules:
                if rule.Name.lower() == old_name.lower() and \
                    (profile is None or rule.Profiles == profile) and \
                        (direction is None or rule.Direction == old_direction):
                    
                    rule.Name = name
                    rule.Description = 'None' if description == '' else description
                    rule.Action = 1 if action == 'Allow' else 0
                    rule.Enabled = enable
                    rule.Direction = 1 if direction == 'Inbound' else 2

                    if protocol == 'TCP':
                        rule.Protocol = 6
                    elif protocol == 'UDP':
                        rule.Protocol = 17
                    else:
                        rule.Protocol = 256
                        
                    if election_port == 'Range':
                        # check value
                        if port is not None and direction == 'Inbound':
                            rule.LocalPorts = str(port)
                        elif port is not None and direction == 'Outbound':
                            rule.RemotePorts = str(port)
                    else: 
                        rule.LocalPorts = ''
                        rule.RemotePorts = ''

                    # check value    
                    if ip:
                        rule.RemoteAddresses = ip
                    else: rule.RemoteAddresses = '*'

                    # check value 
                    if election_program == 'Select':
                        rule.ApplicationName = program
                    else: rule.ApplicationName = '/'


                    self.message.show_message('Se modifico la regla seleccionada', '', self.iconCorrect)

        except Exception as exception:
            com_error_info = exception.excepinfo
            if com_error_info and len(com_error_info) > 5:
                error_code = com_error_info[5]
                error_message = win32api.FormatMessage(error_code)
                print('error 1: ', error_message)
            else:
                print('error 2: ', exception.args[1])


    def get_protocol_name(self, protocol: int) -> str:
        """
        Maps a protocol number to its corresponding name.

        Args:
            protocol (int): The protocol number to be mapped to a name.

        Returns:
            str: The name of the protocol or the input protocol number if no mapping is available.

        Example Usage:
            firewall_rules = Firewall_Rules()
            protocol_name = firewall_rules.get_protocol_name(6)
            print(protocol_name)  # Output: "TCP"

        """
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
        """
        Maps a profile name to its corresponding value.

        Args:
            profile (str): The profile name to be mapped to a value.
            profile (int): The profile value to be mapped to a name.

        Returns:
            int: The numeric value representing the profile or None if no mapping is available.

        Example Usage:
            firewall_rules = Firewall_Rules()
            profile_value = firewall_rules.get_profiles("Private")
            print(profile_value)  # Output: 2

        """
        if isinstance(profile, str):
            profile = profile.lower()
            profile_value = 0  # Inicializa el valor en 0

            if "domain" in profile:
                profile_value += 1
            if "private" in profile:
                profile_value += 2
            if "public" in profile:
                profile_value += 4

            return profile_value

        elif isinstance(profile, int):
            profiles = []
            if profile & 1:
                profiles.append("Domain")
            if profile & 2:
                profiles.append("Private")
            if profile & 4:
                profiles.append("Public")
            return profiles

    def deleteRule(self, name, direction, profile, protocol, port):
        pass
    