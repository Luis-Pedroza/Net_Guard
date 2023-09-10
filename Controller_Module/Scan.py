# ***************************************************
# FILE: Scan.py
#
# DESCRIPTION: 
# This code does a ports scan and returns the obtained data
# It also gets the range of the ports and changes it
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

import psutil
import subprocess
from PyQt5.QtWidgets import QMessageBox
from UI_Module.UI_Message import PopUpMessage


class ScanPorts():
    def __init__(self):
        self.message = PopUpMessage()
        self.icon = QMessageBox.Critical
    # static method to get all the ports in use
    @staticmethod
    def scan_active_ports():
        # initialize a connection of all kinds (TCP & UDP)
        # and an empty list
        connections = psutil.net_connections(kind='all')
        connection_data = []

        # gets each data on the connection
        for data in connections:
            # get the local socket (ip address & port)
            local_address = f"{data.laddr.ip}:{data.laddr.port}"
            # get the remote socket if there´s any (ip address & port)
            remote_address = f"{data.raddr.ip}:{data.raddr.port}" if data.raddr else "-"
            # get the status of the connection
            status = data.status
            # get the PID of the program
            pid = data.pid
            try:
                # gets the name of the program is there is´nt an exception
                program = psutil.Process(pid).name()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                program = "-"
            # gets the protocol used on the socket
            if data.type == 1:
                protocol = "TCP"
            elif data.type == 2:
                protocol = "UDP"
            else:
                protocol = "-" if data.kind != psutil.SOCK_RAW else "RAW"
            # insert the data on the list and return it
            connection_data.append([protocol, local_address, remote_address, status, pid, program])
        return connection_data
    
    # Method to get the range of the ports 
    def get_ports_range(self):
        # command to get tcp and udp range
        command_TCP = 'netsh int ipv4 show dynamicport tcp'
        command_UDP = 'netsh int ipv4 show dynamicport udp'
        try: 
            # execute both commands
            output_TCP = subprocess.run(command_TCP, shell=True, capture_output=True, encoding='cp850')
            output_UDP = subprocess.run(command_UDP, shell=True, capture_output=True, encoding='cp850')
            # if output has an error show an error window
            if output_TCP.returncode != 0 or output_UDP.returncode != 0:
                self.message.show_message('UNABLE_To_get_ports_range',output_TCP.stdout.splitlines()[1], self.icon)
            # else return the output
            else:
                return str(output_TCP.stdout), str(output_UDP.stdout)
        # exception control
        except subprocess.CalledProcessError as exception:
            self.message.show_message('UNABLE_To_Execute_Command_in_get_ports_range', exception, self.icon)

    # Method to change the range of the ports
    def change_ports_range(self, protocol, range):
        status = True
        # change range with first port 49152(dynamic range). IANA recommendation default=16384
        command_range = f'netsh int ipv4 set dynamicport {protocol} start=49152 num={range}'
        try: 
            # execute command
            output_range = subprocess.run(command_range, shell=True, capture_output=True, encoding='cp850')
            # if output has an error show a popUp message and return status false
            if output_range.returncode != 0:
                self.message.show_message('UNABLE_To_change_ports_range', output_range.stdout, self.icon)
                status = False
            # if output does'nt has an error return status true
            else:
                status = True
        # if there's an exception return code False
        except subprocess.CalledProcessError as exception:
            self.message.show_message('UNABLE_To_Execute_Command_in_change_ports_range', exception, self.icon)
            status = False
        finally: return status


                



          
