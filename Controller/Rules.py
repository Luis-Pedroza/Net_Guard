# ***************************************************
# FILE: Rules.py
# -*- coding: utf-8 -*-
#
# DESCRIPTION:
# The FirewallManager class is designed to interact with
# the Windows Firewall, specifically managing rules.
# It provides methods for adding new rules, retrieving rules,
# searching for specific rules, editing existing rules, and more.
# Overall, this class serves as a convenient interface for
# managing Windows Firewall rules programmatically,
# making it easier to create, retrieve, search, and
# edit firewall rules within an application
#
# AUTHOR:  Luis Pedroza
# CREATED: 11/04/2023 (dd/mm/yy)
# ***************************************************

import win32com.client
import win32api
import ipaddress
import os


class FirewallManager():
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
        self.firewall = win32com.client.Dispatch("HNetCfg.FwPolicy2")

    def add_new_rule(self, rule: dict):
        """
        Adds a new firewall rule using the provided parameters.

        Args:
            rule (dict): A dictionary containing the following parameters for the new rule:
            - 'name' (str): The name of the firewall rule.
            - 'description' (str): The description of the firewall rule. If empty, it defaults to 'None'.
            - 'enable' (bool): Whether the rule should be enabled (True) or disabled (False).
            - 'direction' (str): The direction of the rule, 'Inbound' for incoming or 'Outbound' for outgoing traffic.
            - 'action' (str): The action to take for the rule, 'allow' or 'block'.
            - 'protocol' (str): The protocol of the rule, 'TCP', 'UDP', or any other value (defaulting to 'Any').
            - 'port' (str): The selected port option, 'Range' or a specific port.
            - 'selected_port' (str): The port to which the rule applies. If None, it does not specify a port.
            - 'program' (str): The selected program option, 'Select' or None.
            - 'selected_program' (str): The name of the program/application associated with the rule. If None, it does not specify a program.
            - 'ip' (str): The IP address to which the rule applies. If None, it does not specify an IP address.

        Returns:
            None

        Raises:
            Various exceptions if there is an issue while adding the rule.

        Example Usage:
            firewall_rules = FirewallManager()
            new_rule = {
                'name': "MyRule",
                'description': "Allow incoming traffic",
                'enable': "yes",
                'direction': "in",
                'action': "allow",
                'protocol': "TCP",
                'profile': "1",
                'port': "80",
                'selected_port': "Range",
                'program': "my_program.exe",
                'selected_program': "Select",
                'ip': "192.168.1.1"
            }
            firewall_rules.add_new_rule(new_rule)

        """
        try:
            new_rule = win32com.client.Dispatch("HNetCfg.FWRule")
            new_rule.Name = rule['name']
            new_rule.Description = 'None' if rule['description'] == '' else rule['description']
            new_rule.Action = rule['action']
            new_rule.Enabled = rule['enable']
            new_rule.Direction = 1 if rule['direction'] == 0 else 2

            if rule['protocol'] == 'TCP':
                new_rule.Protocol = 6
            elif rule['protocol'] == 'UDP':
                new_rule.Protocol = 17
            else:
                new_rule.Protocol = 256

            profile = rule['profile']
            if profile == 0:
                CurrentProfiles = self.firewall.CurrentProfileTypes
                new_rule.Profiles = CurrentProfiles
            else:
                new_rule.Profiles = profile

            if rule['port'] is not None and rule['direction'] == 0:
                port_value = self.check_port(str(rule['selected_port']))
                if port_value:
                    new_rule.LocalPorts = str(rule['selected_port'])
                else:
                    raise FirewallManagerError('', 'ERROR_PORT_VALUE')
            elif rule['port'] is not None and rule['direction'] == 1:
                port_value = self.check_port(str(rule['selected_port']))
                if port_value:
                    new_rule.RemotePorts = str(rule['selected_port'])
                else:
                    raise FirewallManagerError('', 'ERROR_PORT_VALUE')

            if rule['program'] is not None:
                path = os.path.exists(rule['selected_program'])
                if path:
                    new_rule.ApplicationName = rule['selected_program']
                else:
                    raise FirewallManagerError('', 'ERROR_PATH_VALUE')

            if rule['ip'] is not None:
                ip_value = self.check_ip(rule['ip'])
                if ip_value:
                    new_rule.RemoteAddresses = rule['ip']
                else:
                    raise FirewallManagerError('', 'ERROR_IP_VALUE')

            self.firewall.Rules.Add(new_rule)
        except Exception as exception:
            com_error_info = getattr(exception, 'excepinfo', None)
            if com_error_info and len(com_error_info) > 5:
                error_code = com_error_info[5]
                error_message = win32api.FormatMessage(error_code)
                raise FirewallManagerError('ERROR_win32api_Add: ', str(error_message)) from exception
            else:
                error_message = str(exception)
                raise FirewallManagerError('ERROR_FirewallManager_Add', error_message) from exception
  

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
            firewall_rules = FirewallManager()
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
            raise FirewallManagerError('ERROR_FirewallManager_GET_ALL', str(exception)) from exception  

    def get_searched_rule(self, name: str, profile: int = None, direction: int = None) -> list[list]:
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
            firewall_rules = FirewallManager()
            matching_rules = firewall_rules.get_searched_rule("MyRule", profile="Domain", direction="in")
            for rule in matching_rules:
                print(rule)

        """
        rules = self.firewall.Rules
        rules_list = []
        
        direction = None if direction == 0 else direction
        profile = None if profile == 7 else profile
        try:
            for rule in rules:
                if rule.Name.lower() == name.lower() and \
                    (profile is None or rule.Profiles == profile) and \
                        (direction is None or rule.Direction == direction):
                    rules_list = self.enlist_rules(rule, rules_list)
            return rules_list
        except Exception as exception:
            raise FirewallManagerError('ERROR_FirewallManager_GET_SEARCH', str(exception)) from exception   

    def enlist_rules(self, rule: win32com.client.CDispatch, rules_list: list) -> list:
        """
        Extracts information from a firewall rule and appends it to a list of rules.

        Args:
            rule (win32com.client.CDispatch): The firewall rule from which to extract information.
            rules_list (list): The list of firewall rules to which the extracted information will be appended.

        Returns:
            list: The updated list of firewall rules with the extracted information.

        Example Usage:
            firewall_rules = FirewallManager()
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

    def edit_selected_rule(self, rule_dict: dict):
        """
        Edits a selected firewall rule with the provided parameters.

        Args:
            rule_dict (dict): A dictionary containing the following parameters for the rule:
            - 'old_name' (str): The name of the firewall rule to be edited.
            - 'profile' (str): The profile of the firewall rule.
            - 'old_direction' (str): The old direction of the firewall rule, either 'Inbound' or 'Outbound'.
            - 'name' (str): The new name for the firewall rule.
            - 'description' (str): The new description for the firewall rule.
            - 'enable' (bool): Whether the firewall rule should be enabled.
            - 'direction' (str): The new direction for the firewall rule, either 'Inbound' or 'Outbound'.
            - 'action' (str): The new action for the firewall rule, either 'Allow' or 'Block'.
            - 'protocol' (str): The new protocol for the firewall rule, either 'TCP', 'UDP', or 'Any'.
            - 'port' (str): The new port for the firewall rule.
            - 'election_port' (str): The port election option, either 'Range' or 'Any'.
            - 'program' (str): The new program/application for the firewall rule.
            - 'election_program' (str): The program election option, either 'Select' or 'Any'.
            - 'ip' (str): The new IP address for the firewall rule.

        Returns:
            None

        Raises:
            Various exceptions if there is an issue while editing the rule.

        Example Usage:
            firewall_rules = FirewallManager()
            rule = {
                'old_name': "OldRule",
                'profile': "Private",
                'old_direction': "Inbound",
                'name': "NewRule",
                'description': "Updated description",
                'enable': True,
                'direction': "Outbound",
                'action': "Block",
                'protocol': "TCP",
                'port': "80",
                'election_port': "Range",
                'program': "my_program.exe",
                'election_program': "Select",
                'ip': "192.168.1.2"
            }
            firewall_rules.edit_selected_rule(rule)

        """
        rules = self.firewall.Rules
        try:
            profile = None if self.get_profiles(rule_dict['old_profile']) == 7 else self.get_profiles(rule_dict['old_profile'])
            old_direction = 1 if rule_dict['old_direction'] == 'Inbound' else 2
            port = None if rule_dict['port'] == '' else rule_dict['port']
            program = None if rule_dict['program'] == '' else rule_dict['program']
            for rule in rules:
                if rule.Name.lower() == rule_dict['old_name'].lower() and \
                    (profile is None or rule.Profiles == profile) and \
                        (rule_dict['direction'] is None or rule.Direction == old_direction):
                    rule.Name = rule_dict['name']
                    rule.Description = 'None' if rule_dict['description'] == '' else rule_dict['description']
                    rule.Action = rule_dict['action']
                    rule.Enabled = rule_dict['enable']
                    rule.Direction = 1 if rule_dict['direction'] == 0 else 2

                    if rule_dict['protocol'] == 1:
                        rule.Protocol = 6
                    elif rule_dict['protocol'] == 2:
                        rule.Protocol = 17
                    elif rule_dict['protocol'] == 0:
                        if rule.Protocol == 256:
                            pass
                        else:
                            rule.LocalPorts = ''
                            rule.RemotePorts = ''
                            rule.Protocol = 256

                    new_profile = rule_dict['profile']
                    if new_profile == 0:
                        CurrentProfiles = self.firewall.CurrentProfileTypes
                        rule.Profiles = CurrentProfiles
                    else:
                        rule.Profiles = new_profile

                    if rule_dict['protocol'] == 0 and rule_dict['election_port'] == 0:
                        pass
                    elif rule_dict['election_port'] == 1 and port is not None:
                        if rule_dict['protocol'] == 0:
                            pass
                        elif rule_dict['direction'] == 0:
                            port_value = self.check_port(str(port))
                            if port_value:
                                rule.LocalPorts = str(port)
                            else:
                                raise FirewallManagerError('', 'ERROR_PORT_VALUE')
                        elif rule_dict['direction'] == 1:
                            rule.RemotePorts = str(port)
                    else:
                        rule.LocalPorts = ''
                        rule.RemotePorts = ''

                    if rule_dict['ip']:
                        ip_value = self.check_ip(rule_dict['ip'])
                        if ip_value:
                            rule.RemoteAddresses = rule_dict['ip']
                        else:
                            raise FirewallManagerError('', 'ERROR_IP_VALUE')
                    else: rule.RemoteAddresses = '*'

                    if rule_dict['election_program'] == 'Select':
                        path = os.path.exists(program)
                        if path:
                            rule.ApplicationName = program
                        else:
                            raise FirewallManagerError('', 'ERROR_PATH_VALUE')

        except Exception as exception:
            com_error_info = getattr(exception, 'excepinfo', None)
            if com_error_info and len(com_error_info) > 5:
                error_code = com_error_info[5]
                error_message = win32api.FormatMessage(error_code)
                raise FirewallManagerError('ERROR_win32api_Edit_Rule: ', str(error_message)) from exception
            else:
                error_message = str(exception)
                raise FirewallManagerError('ERROR_FirewallManager_Edit_Rule', error_message) from exception

    def delete_selected_rule(self, name: str, direction: str, profile: str, protocol: str):
        """
        Deletes a selected firewall rule based on the provided parameters.

        Args:
            name (str): The name of the firewall rule to be deleted.
            direction (str): The direction of the firewall rule, either 'Inbound' or 'Outbound'.
            profile (str): The profile of the firewall rule.
            protocol (str): The protocol of the firewall rule.

        Returns:
            None

        Raises:
            Various exceptions if there is an issue while deleting the rule.

        Example Usage:
            firewall_rules = FirewallManager()
            firewall_rules.delete_selected_rule("MyRule", "Inbound", "Private", "TCP")

        Note:
            HNetCfg.FwPolicy2 can delete only by name, so this method will delete
            all rules with the given name. It does not use any other parameters

        """
        rules = self.firewall.Rules
        try:
            for rule in rules:
                if rule.Name.lower() == name.lower():
                    rules.Remove(rule.Name)
        except Exception as exception:
            com_error_info = getattr(exception, 'excepinfo', None)
            if com_error_info and len(com_error_info) > 5:
                error_code = com_error_info[5]
                error_message = win32api.FormatMessage(error_code)
                raise FirewallManagerError('ERROR_win32api_Delete_Rule: ', str(error_message)) from exception
            else:
                error_message = str(exception)
                raise FirewallManagerError('ERROR_FirewallManager_Delete_Rule', error_message) from exception

    def get_protocol_name(self, protocol: int) -> str:
        """
        Maps a protocol number to its corresponding name.

        Args:
            protocol (int): The protocol number to be mapped to a name.

        Returns:
            str: The name of the protocol or the input protocol number if no mapping is available.

        Example Usage:
            firewall_rules = FirewallManager()
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
            firewall_rules = FirewallManager()
            profile_value = firewall_rules.get_profiles("Private")
            print(profile_value)  # Output: 2

        """
        if isinstance(profile, str):
            profile = profile.lower()
            profile_value = 0

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
        
    def check_port(self, input_str: str):
        input_str = input_str.strip()
        values = input_str.split(',')
        
        for value in values:
            if '-' in value:
                start, end = value.split('-')
                if start.isdigit() and end.isdigit():
                    start, end = int(start), int(end)
                    if start <= end:
                        continue
            elif value.isdigit():
                continue
            return False
        return True

    def check_ip(self, ip_str: str):
        ip_parts = ip_str.split("-")
        if len(ip_parts) == 2:
            start_ip_str, end_ip_str = ip_parts
            start_ip = ipaddress.ip_address(start_ip_str.strip())
            end_ip = ipaddress.ip_address(end_ip_str.strip())
            if start_ip <= end_ip:
                return True
        else:
            ipaddress.ip_address(ip_str.strip())
            return True
        return False


class FirewallManagerError(Exception):
    def __init__(self, error_code, error_description):
        super().__init__(error_description)
        self.error_code = error_code