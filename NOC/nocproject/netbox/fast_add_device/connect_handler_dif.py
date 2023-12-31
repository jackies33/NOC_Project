


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
                     location = None,device_role = None,tenants = None,conn_scheme = None,management = None,
                     racks = None):

            self.ip_conn = ip_conn
            self.mask = mask
            self.platform = platform
            self.site_name = site_name
            self.location = location
            self.device_role = device_role
            self.tenants = tenants
            self.conn_scheme = conn_scheme
            self.management = management
            self.racks = racks


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
                                adding = ADD_NB(device_name, self.site_name,self.location, self.tenants, self.device_role,manufacturer,
                                                           self.platform, device_type, primary_ip, interface_name,self.conn_scheme,self.management, self.racks)
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

                            value_xml = etree.tostring(config, encoding='unicode', pretty_print=True)
                            root = etree.fromstring(value_xml)
                            interface_name = ''
                            primary_ip = (f'{self.ip_conn}/{self.mask}')
                            #print('this is connect_to_device_juniper_middle!!!!')
                            for interface in root.xpath('//interface'):
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

                            dev.close()
                            manufacturer = 'Juniper Networks'
                            device_type = classifier_device_type(manufacturer,device_type)
                            #print('this is connect_to_device_juniper_out!!!!')
                            adding = ADD_NB(device_name, self.site_name, self.location , self.tenants, self.device_role, manufacturer,
                                       self.platform , device_type, primary_ip, interface_name,self.conn_scheme,self.management, self.racks)
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
                                adding = ADD_NB(device_name, self.site_name,self.location, self.tenants, self.device_role,manufacturer,
                                                           self.platform, device_type, primary_ip, interface_name,self.conn_scheme,self.management, self.racks)
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
                manufacturer = 'Fortinet'
                device_type = classifier_device_type(manufacturer,device_type)
                ssh1.close()
                adding = ADD_NB(device_name, self.site_name, self.location, self.tenants, self.device_role,
                                manufacturer,
                                self.platform, device_type, primary_ip, interface_name, self.conn_scheme,
                                self.management, self.racks)
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
                        adding = ADD_NB(device_name, self.site_name,self.location, self.tenants, self.device_role,manufacturer,
                                                   self.platform, device_type, primary_ip, interface_name,self.conn_scheme,self.management, self.racks)
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
                                adding = ADD_NB(device_name, self.site_name,self.location, self.tenants, self.device_role,manufacturer,
                                                           self.platform, device_type, primary_ip, interface_name,self.conn_scheme,self.management, self.racks)
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
                   adding = ADD_NB(device_name, self.site_name, self.location, self.tenants, self.device_role,
                                   manufacturer,
                                   self.platform, device_type, primary_ip, interface_name, self.conn_scheme,
                                   self.management, self.racks)
                   result = adding.add_device()
                   return result
               except Exception as err:
                   print(f"Error {err}")
                   return [False, err]


if __name__ == '__main__':
     print('__main__')

