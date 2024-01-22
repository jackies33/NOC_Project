


import socket
from .add_device import ADD_NB
from .classifier import classifier_device_type
from .my_pass import mylogin , mypass ,rescue_login, rescue_pass
from netmiko import ConnectHandler , NetMikoAuthenticationException, NetMikoTimeoutException
import re
from jnpr.junos.exception import ConnectAuthError,ConnectClosedError,ConnectError,ConnectTimeoutError
from jnpr.junos import Device
from lxml import etree
import time
import paramiko
from paramiko import SSHException
from airwaveapiclient import AirWaveAPIClient
import datetime


login = mylogin
password = mypass

class CONNECT_HANDLER():

        """
        Class for connection to different device
        """

        def __init__(self, ip_conn = None,mask = None,platform = None,site_name = None,
                     location = None,device_role = None,tenants = None,conn_scheme = None,
                     racks = None ,stack_enable = None):

            self.ip_conn = ip_conn
            self.mask = mask
            self.platform = platform
            self.site_name = site_name
            self.location = location
            self.device_role = device_role
            self.tenants = tenants
            self.conn_scheme = conn_scheme
            self.racks = racks
            self.management = 1
            self.stack_enable = stack_enable


        def check_ssh(self,ip_conn):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip_conn, 22))
            scheme = 0
            if result == 0:
                     scheme = 'ssh'
            else:
                result = sock.connect_ex((ip_conn, 23))
                if result == 0:
                     scheme = 'telnet'
                else:
                  scheme = 0
            sock.close()
            return scheme


        def template_conn(self,ip_conn,type_device_for_conn,conn_scheme):
            if conn_scheme == "ssh":
                host1 = {

                    "host": ip_conn,
                    "username": login,
                    "password": password,
                    "device_type": type_device_for_conn,
                    "global_delay_factor": 0.5,
                }
            else:
                host1 = {

                    "host": ip_conn,
                    "username": login,
                    "password": password,
                    "device_type": type_device_for_conn,
                    "global_delay_factor": 3,
                    "port": 23
                }
            return host1


        def conn_Huawei(self,*args):

               type_device_for_conn = 'huawei'
               host1 = self.template_conn(self.ip_conn,type_device_for_conn,self.conn_scheme)

               try:

                        with ConnectHandler(**host1) as net_connect:
                                primary_ip = (f'{self.ip_conn}/{self.mask}')
                                output_name_result = net_connect.send_command('display current-configuration | include sysname',
                                                                              delay_factor=.5)  # command result
                                device_name = re.findall(r"sysname \S+", output_name_result)[0].split('sysname ')[1]
                                output_version = net_connect.send_command('display version',
                                                                          delay_factor=.5)
                                command_ip = (f'display ip interface brief  | include {self.ip_conn}')
                                output_ip = net_connect.send_command(command_ip, delay_factor=.5)
                                escaped_ip_address = re.escape(self.ip_conn)
                                re_ip = (f"(\S+)\s+{escaped_ip_address}")
                                interface_name = re.findall(re_ip, output_ip)[0]
                                manufacturer = 'Huawei Technologies Co.'
                                device_type = classifier_device_type(manufacturer,re.findall(r'NE20E-S2F|AR6120|NetEngine 8000 F1A-8H20Q'
                                                                                r'|S5700-28C-EI-24S|S5735-S48S4X|CE8851-32CQ8DQ-P|CE6881-48S6CQ', output_version)[0])
                                # print(device_name,device_type,interface_name)
                                net_connect.disconnect()

                                list_serial_devices = []
                                if self.stack_enable == True:
                                    output_stack = net_connect.send_command('display stack', delay_factor=.5)
                                    slave_output = re.findall(r"\d\s+Slave", output_stack)
                                    standby_output = re.findall(r"\d\s+Standby", output_stack)
                                    master_output = re.findall(r"\d\s+Master", output_stack)
                                    for slave in slave_output:
                                        member_id = slave.replace(" ", "").split('Slave')[0]
                                        list_serial_devices.append(
                                            {'member_id': member_id, 'sn_number': '', 'master': False})
                                    for standby in standby_output:
                                        member_id = standby.replace(" ", "").split('Standby')[0]
                                        list_serial_devices.append(
                                            {'member_id': member_id, 'sn_number': '', 'master': False})
                                    for master in master_output:
                                        member_id = master.replace(" ", "").split('Master')[0]
                                        list_serial_devices.append(
                                            {'member_id': member_id, 'sn_number': '', 'master': True})
                                    output_manufacturer = net_connect.send_command('display device manufacture-info', delay_factor=.5)
                                    member_output = re.findall(f'^\d\s+-\s+\S+', output_manufacturer, re.MULTILINE)
                                    for member in member_output:
                                            member_id = re.findall(r'\d\s+-\s+', member)[0].replace(" ", "")[0]
                                            member_sn = re.findall(r'-\s+\S+', member)[0].replace(" ", "").split("-")[1]
                                            for l in list_serial_devices:
                                                if l['member_id'] == member_id:
                                                    l['sn_number'] = member_sn

                                elif self.stack_enable == False:
                                    output_sn_main = net_connect.send_command('display device manufacture-info', delay_factor=.5)
                                    if "Error" in output_sn_main:
                                        output_sn_main = net_connect.send_command('display esn', delay_factor=.5)
                                        member_sn = re.findall(f'ESN.+:\s+\S+', output_sn_main)[0].split(':')[1].replace(" ", "")
                                        list_serial_devices.append({'member_id': 0, 'sn_number': member_sn, 'master': False})
                                    else:
                                        member_output = re.findall(f'^\d\s+-\s+\S+', output_sn_main, re.MULTILINE)
                                        for member in member_output:
                                            member_sn = re.findall(r'\d\s+-\s+\S+', output_sn_main)[0].replace(" ", "").split("-")[1]
                                            list_serial_devices.append(
                                                {'member_id': 0, 'sn_number': member_sn, 'master': False})


                                adding = ADD_NB(device_name, self.site_name, self.location, self.tenants,
                                                self.device_role,
                                                manufacturer, self.platform, device_type[0], primary_ip, interface_name,
                                                self.conn_scheme, self.management, self.racks, list_serial_devices,
                                                self.stack_enable)
                                result = adding.add_device()
                                return result


               except (NetMikoAuthenticationException, NetMikoTimeoutException) as err:  # exceptions
                    print('\n\n not connect to ' + self.ip_conn + '\n\n')
                    return [False, err]
               except Exception as err:
                   print(f"Error {err}")
                   return [False, err]

        def conn_Juniper_rpc(self,*args):
            #print('this is connect_to_device_juniper!!!!')
            #host1 = self.template_conn(ip_conn,manufacturer)
            i=0
            dev = Device(host=self.ip_conn, user=mylogin, password=mypass)
            result = [False, 'start']
            while i<2:
                    try:
                                dev.open()
                    except Exception as err:
                         print(f"Error {err}")
                         dev = Device(host=self.ip_conn, user=rescue_login, password=rescue_pass)
                         i = i + 1
                         continue

                    else:
                        try:

                            device_name = dev.facts['hostname']
                            device_type = dev.facts['model']
                            config = dev.rpc.get_config(filter_xml=etree.XML(f'''
                                         <configuration>
                                             <interfaces>
                                                 <interface>
                                                    <unit>
                                                       <family>
                                                          <inet>
                                                             <address>
                                                                <name>{self.ip_conn}/{self.mask}</name>
                                                             </address>
                                                          </inet>
                                                       </family>
                                                    </unit>
                                                 </interface>
                                             </interfaces>
                                         </configuration>'''),
                                                        options={'database': 'committed', 'inherit': 'inherit'})

                            interface_name = ''
                            primary_ip = (f'{self.ip_conn}/{self.mask}')
                            #print('this is connect_to_device_juniper_middle!!!!')
                            for interface in config.xpath('//interface'):
                                interface_name = interface.find('name').text
                                for unit in interface.xpath('.//unit'):
                                    unit = unit.find('name').text
                                    if interface_name == 'fxp0':
                                        break
                                    if interface_name == 'vlan':
                                        interface_name = interface_name + unit
                                    if interface_name == 'irb':
                                        interface_name = (f'{interface_name}.{unit}')
                                    if unit == '0':
                                        break
                                    else:
                                        break
                            list_serial_devices = []
                            if self.stack_enable == True:
                                memb_count = 0
                                vc_info = dev.rpc.get_virtual_chassis_information()
                                # print(etree.tounicode(vc_info))
                                # vc_mode = vc_info.find('.//virtual-chassis-mode').text
                                members = vc_info.findall('.//member')
                                # if vc_mode == 'Enabled':
                                for member in members:
                                    member_id = int(member.find('member-id').text)
                                    member_serial_number = member.find('member-serial-number').text
                                    role = member.find('member-role').text
                                    if role == "Master*":
                                        member_role = True
                                    else:
                                        member_role = False
                                    # print(f"Member ID: {member_id}, Serial Status: {member_serial_status}")
                                    memb_count = memb_count + 1
                                    list_serial_devices.append(
                                        {'member_id': member_id, 'sn_number': member_serial_number,
                                         'master': member_role})
                                if memb_count == 1:
                                    self.stack_enable = False
                                elif memb_count > 1:
                                    self.stack_enable = True
                            elif self.stack_enable == False:
                                inventory = dev.rpc.get_chassis_inventory()
                                serial_number = str(inventory.findtext('.//serial-number'))
                                list_serial_devices.append(
                                    {'member_id': 0, 'sn_number': serial_number, 'master': False})
                            dev.close()
                            manufacturer = 'Juniper Networks'
                            device_type = classifier_device_type(manufacturer,device_type)
                            adding = ADD_NB(device_name, self.site_name, self.location , self.tenants, self.device_role,
                                            manufacturer,self.platform , device_type[0], primary_ip, interface_name,
                                            self.conn_scheme,self.management, self.racks, list_serial_devices, self.stack_enable)
                            result = adding.add_device()
                            break
                        except Exception as err:
                            print(err)
                            return [False, err]
            return result




        def conn_Cisco_IOS(self,*args):
               type_device_for_conn = "cisco_ios"
               host1 = self.template_conn(self.ip_conn, type_device_for_conn,self.conn_scheme)
               try:
                        with ConnectHandler(**host1) as net_connect:
                                primary_ip = (f'{self.ip_conn}/{self.mask}')
                                output_main = net_connect.send_command('show version', delay_factor=.5)
                                device_name = re.findall(f"\S+ uptime is", output_main)[0].split("uptime is")[0].strip()
                                manufacturer = 'Cisco Systems'
                                device_type = classifier_device_type(manufacturer,re.findall(f"^cisco \S+", output_main,re.MULTILINE)[0].split("cisco")[1].strip())
                                output_interface_name = net_connect.send_command(f'show ip interface brief | include {self.ip_conn}', delay_factor=.5)
                                interface_name = re.findall(f"^\S+\s+{self.ip_conn}", output_interface_name, re.MULTILINE)[0].split(self.ip_conn)[0].strip()
                                list_serial_devices = []
                                if self.stack_enable == True:
                                    output_switch = net_connect.send_command('show switch', delay_factor=.5)
                                    member_output = re.findall(r"\d\s+Member \S+", output_switch)
                                    master_output = re.findall(r"\d\s+Master \S+", output_switch)[0]
                                    for member in member_output:
                                        member_id = member.replace(" ", "").split('Member')[0]
                                        list_serial_devices.append(
                                            {'member_id': member_id, 'sn_number': '',
                                             'master': False})

                                    master_id = master_output.replace(" ", "").split('Master')[0]
                                    list_serial_devices.append(
                                        {'member_id': master_id, 'sn_number': '',
                                         'master': True})

                                    output_inventory = net_connect.send_command('show inventory', delay_factor=.5)
                                    member_output = re.findall(f'^NAME:.+\nPID: {device_type[1]}.+SN: \S+', output_inventory,
                                                               re.MULTILINE)
                                    for member in member_output:
                                        member_id = re.findall(r'NAME: "\d"', member)[0].split('NAME: "')[1].split('"')[
                                            0]
                                        member_sn = re.findall(r'SN: \S+', member)[0].split('SN: ')[1]
                                        for l in list_serial_devices:
                                            if l['member_id'] == member_id:
                                                l['sn_number'] = member_sn

                                elif self.stack_enable == False:
                                    serial_number = re.findall(f'Processor board ID \S+', output_main)[0].split('Processor board ID ')[1]
                                    list_serial_devices.append(
                                        {'member_id': 0, 'sn_number': serial_number, 'master': False})

                                adding = ADD_NB(device_name, self.site_name, self.location, self.tenants,
                                                self.device_role,
                                                manufacturer, self.platform, device_type[0], primary_ip, interface_name,
                                                self.conn_scheme, self.management, self.racks, list_serial_devices,
                                                self.stack_enable)
                                result = adding.add_device()
                                net_connect.disconnect()
                                return result

               except (NetMikoAuthenticationException, NetMikoTimeoutException) as err:  # exceptions
                    print('\n\n not connect to ' + self.ip_conn + '\n\n')
                    return [False, err]
               except Exception as err:
                   print(f"Error {err}")
                   return [False, err]

        def conn_FortiGate(self, *args):

            primary_ip = (f'{self.ip_conn}/{self.mask}')
            cmnd1 = '\n config global \n\n      '  # Commands
            cmnd2 = '\n get system status  \n\n           '  # Commands
            cmnd3 = '\n get system interface physical  \n\n        '  # Commands
            cmnd4 = '         \n\n           '
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip_conn,
                        username=login,
                        password=password,
                        look_for_keys=False)
            ssh1 = ssh.invoke_shell()
            list_serial_devices = []
            try:
                time.sleep(1)
                ssh1.send(cmnd1)
                time.sleep(1)
                ssh1.send(cmnd2)
                time.sleep(1)
                ssh1.send(cmnd3)
                time.sleep(1)
                ssh1.send(cmnd4)
                time.sleep(1)
                output1 = (ssh1.recv(9999999).decode("utf-8"))
                time.sleep(1)
                device_name = re.findall(f"Hostname: \S+", output1)[0].split("Hostname: ")[1]
                interface_name = re.findall(f"==.+\n.+\n\s+ip: {self.ip_conn}", output1)[0]
                interface_name = re.findall(f"==\[\S+\]", interface_name)[0].split("==[")[1].rsplit(']')[0]
                device_type = re.findall(f"Version: \S+", output1)[0].split("Version: ")[1]
                member_sn = re.findall(r'Serial-Number: \S+', output1)[0].split("Serial-Number: ")[1]
                list_serial_devices.append({'member_id': 0, 'sn_number': member_sn, 'master': False})
                manufacturer = 'Fortinet'
                device_type = classifier_device_type(manufacturer,device_type)
                ssh1.close()
                adding = ADD_NB(device_name, self.site_name, self.location, self.tenants, self.device_role,
                                manufacturer, self.platform, device_type[0], primary_ip, interface_name,
                                self.conn_scheme, self.management, self.racks, list_serial_devices, self.stack_enable)
                result = adding.add_device()
                return result
            except Exception as err:
                print(f'\n\n{datetime.datetime.now()}\n\n{err}')
                return [False, err]



        def conn_IBM_lenovo_sw(self,*args):
            primary_ip = (f'{self.ip_conn}/{self.mask}')
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cmnd1 = 'en\n'
            cmnd2 = '\nshow system\n\n\n\n'
            ssh.connect(self.ip_conn,
                        username=mylogin,
                        password=mypass,
                        look_for_keys=False,
                        allow_agent=False)
            try:
                        ssh1 = ssh.invoke_shell()
                        time.sleep(4)
                        ssh1.send(cmnd1)
                        time.sleep(1)
                        ssh1.send(cmnd2)
                        time.sleep(1)
                        output_name_result = (ssh1.recv(65535).decode("utf-8"))
                        time.sleep(3)
                        ssh1.close()
                        preresult1 = re.findall(r'sysName:     \S+', output_name_result)[0].split('sysName:     ')[1]
                        device_name = preresult1.split('"')[1]
                        manufacturer = 'LENOVO'
                        device_type = classifier_device_type(manufacturer,re.findall(r'Flex System Fabric EN4093R 10Gb Scalable Switch', output_name_result))
                        interface_name = 'EXTM'
                        list_serial_devices = []
                        member_sn = re.findall(r'Serial Number\s+:\s+\S+', output_name_result)[0].split(":")[1].split(".")[0]
                        list_serial_devices.append({'member_id': 0, 'sn_number': member_sn, 'master': False})
                        adding = ADD_NB(device_name, self.site_name, self.location, self.tenants, self.device_role,
                                        manufacturer, self.platform, device_type[0], primary_ip, interface_name,
                                        self.conn_scheme, self.management, self.racks, list_serial_devices,
                                        self.stack_enable)
                        result = adding.add_device()
                        return result
            except IndexError as err:
                        print(f"\n\n\n{err}\n\n\n")
                        return [False, err]
            except SSHException as err:
                        print(f"\n\n\n{err}\n\n\n")
                        return [False, err]
            except Exception as err:
                        print(f"Error {err}")
                        return [False, err]

        def conn_Cisco_NXOS(self,*args):
               type_device_for_conn = "cisco_nxos"
               host1 = self.template_conn(self.ip_conn, type_device_for_conn,self.conn_scheme)
               try:
                        with ConnectHandler(**host1) as net_connect:
                                primary_ip = (f'{self.ip_conn}/{self.mask}')
                                output1 = net_connect.send_command('show hostname', delay_factor=.5)
                                device_name = re.findall(r'\S+', output1)[0]
                                output2 = net_connect.send_command('show version',delay_factor=.5)  # command result
                                output_name_result = re.findall(r'Hardware\n.+', output2)[0]
                                manufacturer = 'Cisco Systems'
                                device_type = classifier_device_type(manufacturer,re.findall(r'cisco Nexus7700 C7702|cisco Nexus 6001', output_name_result)[0].split("cisco")[1].strip())
                                interface_name = 'mgmt0'
                                list_serial_devices = []
                                serial_number = re.findall(f'Processor board ID \S+', output2)[0].split('Processor board ID ')[1]
                                list_serial_devices.append({'member_id': 0, 'sn_number': serial_number, 'master': False})
                                adding = ADD_NB(device_name, self.site_name, self.location, self.tenants,
                                                self.device_role,
                                                manufacturer, self.platform, device_type[0], primary_ip, interface_name,
                                                self.conn_scheme, self.management, self.racks, list_serial_devices,
                                                self.stack_enable)
                                result = adding.add_device()
                                net_connect.disconnect()
                                return result

               except (NetMikoAuthenticationException, NetMikoTimeoutException) as err:  # exceptions
                    print('\n\n not connect to ' + self.ip_conn + '\n\n')
                    return [False, err]
               except Exception as err:
                   print(f"Error {err}")
                   return [False, err]



        def conn_AWMP(self,*args):
               airwave = AirWaveAPIClient(username=mylogin, password=mypass, url=f'https://{self.ip_conn}')
               try:
                   airwave.login()
                   output = airwave.amp_stats().text
                   manufacturer = "Hewlett Packard Enterprise"
                   device_type = classifier_device_type(manufacturer,re.findall("<name>.*</name>", output)[0].split('<name>')[1].split('</name>'))
                   primary_ip = (f'{self.ip_conn}/{self.mask}')
                   interface_name = "VirtInt"
                   device_name = f'AWMP_{self.ip_conn}'
                   list_serial_devices = []
                   list_serial_devices.append({'member_id': 0, 'sn_number': "NNNNNNN000000", 'master': False})
                   adding = ADD_NB(device_name, self.site_name, self.location, self.tenants, self.device_role,
                                   manufacturer, self.platform, device_type[0], primary_ip, interface_name,
                                   self.conn_scheme, self.management, self.racks, list_serial_devices,
                                   self.stack_enable)
                   result = adding.add_device()
                   return result
               except Exception as err:
                   print(f"Error {err}")
                   return [False, err]

        def conn_OS_Linux(self,*args):
            type_device_for_conn = "linux"
            host1 = self.template_conn(self.ip_conn, type_device_for_conn, self.conn_scheme)
            try:
                with ConnectHandler(**host1) as net_connect:
                    primary_ip = (f'{self.ip_conn}/{self.mask}')
                    sudo = net_connect.send_command('sudo -s', delay_factor=.5, expect_string="#")
                    output_hostname = net_connect.send_command('cat /etc/hostname', delay_factor=.5, expect_string="#")
                    device_name = re.findall(r'\S+', output_hostname)[0]
                    output_interface = net_connect.send_command('ip a', delay_factor=.5, expect_string="#")
                    interface_name = re.findall(f'^\d+: .+\n.+\n.+inet {self.ip_conn}', output_interface, re.MULTILINE)[0]
                    interface_name = re.findall(r'\d+: \S+:', interface_name)[0].split(":")[1].strip()
                    output_device_type = net_connect.send_command('cat /etc/issue', delay_factor=.5, expect_string="#")
                    manufacturer = 'Meinberg Funkuhren GmbH & Co. KG'
                    device_type = classifier_device_type(manufacturer, re.findall(r'Meinberg LANTIME OS7|Ubuntu', output_device_type)[0])
                    list_serial_devices = []
                    list_serial_devices.append({'member_id': 0, 'sn_number': "NNNNNNN000000", 'master': False})
                    adding = ADD_NB(device_name, self.site_name, self.location, self.tenants, self.device_role,
                                    manufacturer, self.platform, device_type[0], primary_ip, interface_name,
                                    self.conn_scheme, self.management, self.racks, list_serial_devices,
                                    self.stack_enable)
                    result = adding.add_device()
                    return result


            except Exception as err:
                print(f"Error {err}")
                return [False, err]




if __name__ == '__main__':
     print('__main__')

