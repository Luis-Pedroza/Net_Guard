# ***************************************************
# FILE: Scan.py
#
# DESCRIPTION:
# The program encapsulates functionality for managing network ports and port ranges.
# It allows users to scan and retrieve information about active network connections,
# such as protocol, local and remote addresses, status, process IDs, and program names.
# Additionally, it provides features to query and modify the range of dynamic ports
# for TCP and UDP protocols.
#
# AUTHOR:  Luis Pedroza
# CREATED: 16/03/2023 (dd/mm/yy)
# ***************************************************

import psutil
import subprocess


class ScanPorts():
    """
    A class for scanning and managing active network ports and port ranges.

    Attributes:
        None

    Methods:
        scan_active_ports():
            Static method to retrieve information about all active network connections,
            including protocol, local and remote addresses, status, process ID, and program name.

        get_ports_range():
            Method to retrieve the current range of dynamic ports for TCP and UDP protocols.
            It uses system commands to get the port range information.

        change_ports_range(protocol: str, range: int) -> bool:
            Method to change the range of dynamic ports for a specified protocol (TCP or UDP).
            It uses a system command to modify the port range.

    """
    @staticmethod
    def scan_active_ports() -> list:
        """
        Static method to retrieve information about all active network connections.

        Args:
            None

        Returns:
            list: A list of lists containing connection data, including protocol,
                  local address, remote address, status, process ID, and program name.

        Raises:
            Various exceptions if there is an issue while getting the data

        Example Usage:
            active_ports = ScanPorts.scan_active_ports()
            for port_info in active_ports:
                print(port_info)

        """
        try:
            connections = psutil.net_connections(kind='all')
            connection_data = []
            for data in connections:
                local_address = f"{data.laddr.ip}:{data.laddr.port}"
                remote_address = f"{data.raddr.ip}:{data.raddr.port}" if data.raddr else "-"
                status = data.status
                pid = data.pid
                try:
                    program = psutil.Process(pid).name()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    program = "-"
                if data.type == 1:
                    protocol = "TCP"
                elif data.type == 2:
                    protocol = "UDP"
                else:
                    protocol = "-" if data.kind != psutil.SOCK_RAW else "RAW"
                connection_data.append([protocol, local_address, remote_address, status, pid, program])
            return connection_data
        except psutil.Error as exception:
            raise ScanError('ERROR: Scan_psutil_ActivePorts', str(exception))
        except Exception as exception:
            raise ScanError('ERROR: Scan_ActivePorts', str(exception))

    def get_ports_range(self) -> list:
        """
        Static method to retrieve information about all active network connections.

        Args:
            None

        Returns:
            list: A list of lists containing connection data, including protocol,
                  local address, remote address, status, process ID, and program name.

        Raises:
            Various exceptions if there are errors while retrieving process names.

        Example Usage:
            active_ports = ScanPorts.scan_active_ports()
            for port_info in active_ports:
                print(port_info)

        """
        try:
            command_TCP = 'netsh int ipv4 show dynamicport tcp'
            command_UDP = 'netsh int ipv4 show dynamicport udp'
            output_TCP = subprocess.run(command_TCP, shell=True, capture_output=True, encoding='cp850')
            output_UDP = subprocess.run(command_UDP, shell=True, capture_output=True, encoding='cp850')
            if output_TCP.returncode != 0:
                raise ScanError('command error TCP', str(output_TCP.returncode))
            elif output_UDP.returncode != 0:
                raise ScanError('command error UDP', str(output_UDP.returncode))
            else:
                return str(output_TCP.stdout), str(output_UDP.stdout)
        except subprocess.CalledProcessError as exception:
            raise ScanError('ERROR: Scan_subprocess_GetRange', str(exception))
        except Exception as exception:
            raise ScanError('ERROR: Scan_GetRange', str(exception))

    def change_ports_range(self, protocol: str, range: int) -> bool:
        """
        Method to change the range of dynamic ports for a specified protocol (TCP or UDP).

        Args:
            protocol (str): The protocol for which to change the port range ('TCP' or 'UDP').
            range (int): The new port range to set.

        Returns:
            bool: True if the port range was successfully changed; False otherwise.

        Raises:
            Various exceptions if there are errors while executing system commands.

        Example Usage:
            if scan_ports.change_ports_range('TCP', 10000):
                print("TCP Port Range successfully changed.")
            else:
                print("Failed to change TCP Port Range.")

        """
        status = True
        # change range with first port 49152(dynamic range). IANA recommendation default=16384
        command_range = f'netsh int ipv4 set dynamicport {protocol} start=49152 num={range}'
        try:
            output_range = subprocess.run(command_range, shell=True, capture_output=True, encoding='cp850')
            if output_range.returncode != 0:
                status = False
            else:
                status = True
            return status
        except subprocess.CalledProcessError as exception:
            raise ScanError('ERROR: Scan_subprocess_ChangeRange', str(exception))
        except Exception as exception:
            raise ScanError('ERROR: Scan_ChangeRange', str(exception))


class ScanError(Exception):
    def __init__(self, error_code, error_description):
        super().__init__(error_description)
        self.error_code = error_code
