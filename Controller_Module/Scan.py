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
from UI_Module.UI_Error import PopUp_Messages


class Scan_Ports():
    def __init__(self):
        self.message = PopUp_Messages()
        self.icon = QMessageBox.Critical
    # static method to get all the ports in use
    @staticmethod
    def scanAll():
        # initialize a connection of all kinds (TCP & UDP)
        # and an empty list
        connections = psutil.net_connections(kind='all')
        connection_data = []

        # gets each data on the connection
        for data in connections:
            # get the local socket (ip address & port)
            localAddress = f"{data.laddr.ip}:{data.laddr.port}"
            # get the remote socket if there´s any (ip address & port)
            remoteAddress = f"{data.raddr.ip}:{data.raddr.port}" if data.raddr else "-"
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
            connection_data.append([protocol, localAddress, remoteAddress, status, pid, program])
        return connection_data
    
    # Method to get the range of the ports 
    def getRange(self):
        # command to get tcp and udp range
        commandTCP = 'netsh int ipv4 show dynamicport tcp'
        commandUDP = 'netsh int ipv4 show dynamicport udp'
        try: 
            # execute both commands
            outputTCP = subprocess.run(commandTCP, shell=True, capture_output=True, encoding='cp850')
            outputUDP = subprocess.run(commandUDP, shell=True, capture_output=True, encoding='cp850')
            # if output has an error show an error window
            if outputTCP.returncode != 0 or outputUDP.returncode != 0:
                self.message.showMessage('UNABLE_To_getRange',outputTCP.stdout.splitlines()[1], self.icon)
            # else return the output
            else:
                return str(outputTCP.stdout), str(outputUDP.stdout)
        # exception control
        except subprocess.CalledProcessError as exception:
            self.message.showMessage('UNABLE_To_Execute_Command_in_getRange', exception, self.icon)

    # Method to change the range of the ports
    def changeRange(self, protocol, range):
        status = True
        # change range with first port 49152(dynamic range). IANA recommendation default=16384
        commandRange = f'netsh int ipv4 set dynamicport {protocol} start=49152 num={range}'
        try: 
            # execute command
            outputRange = subprocess.run(commandRange, shell=True, capture_output=True, encoding='cp850')
            # if output has an error show a popUp message and return status false
            if outputRange.returncode != 0:
                self.message.showMessage('UNABLE_To_changeRange', outputRange.stdout, self.icon)
                status = False
            # if output does'nt has an error return status true
            else:
                status = True
        # if there's an exception return code False
        except subprocess.CalledProcessError as exception:
            self.message.showMessage('UNABLE_To_Execute_Command_in_changeRange', exception, self.icon)
            status = False
        finally: return status


                



          
