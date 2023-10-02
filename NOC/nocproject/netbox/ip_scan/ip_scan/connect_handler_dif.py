

import socket
from .add_device import ADD_NB
from .classifier import classifier_device_type
from .my_pass import mylogin , mypass
from netmiko import ConnectHandler , NetMikoAuthenticationException, NetMikoTimeoutException
import re
from jnpr.junos.exception import ConnectAuthError,ConnectClosedError,ConnectError,ConnectTimeoutError
from jnpr.junos import Device
from lxml import etree
import time
import paramiko
from paramiko import SSHException


login = mylogin
password = mypass

class CONNECT_DEVICE():

        """
        Class for connection to different device
        """

        def __init__(self, ip_conn = None,mask = None,platform = None,site_name = None,
                     location = None,device_role = None,tenants = None,conn_scheme = None,management = None):

            self.ip_conn = ip_conn
            self.mask = mask
            self.platform = platform
            self.site_name = site_name
            self.location = location
            self.device_role = device_role
            self.tenants = tenants
            self.conn_scheme = conn_scheme
            self.management = management


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




        def template_conn(self,ip_conn,type_device_for_conn):

                host1 = {

                    "host": ip_conn,
                    "username": login,
                    "password": password,
                    "device_type": type_device_for_conn,
                    "global_delay_factor": 0.5,
                }
                return host1

        def conn_Huawei(self,*args):

               type_device_for_conn = 'huawei'
               host1 = self.template_conn(self.ip_conn,type_device_for_conn)


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
                                device_type = classifier_device_type(re.findall(r'NE20E-S2F|AR6120|NetEngine 8000 F1A-8H20Q', output_version)[0])
                                # print(device_name,device_type,interface_name)
                                net_connect.disconnect()
                                manufacturer = 'huawei-technologies-co'
                                adding = ADD_NB(device_name, self.site_name,self.location, self.tenants, self.device_role,manufacturer,
                                                           self.platform, device_type, primary_ip, interface_name,self.conn_scheme,self.management)
                                adding.add_device()


               except (NetMikoAuthenticationException, NetMikoTimeoutException):  # exceptions
                    print('\n\n not connect to ' + self.ip_conn + '\n\n')


        def conn_Juniper_rpc(self,*args):

               print('this is connect_to_device_juniper!!!!')
               #host1 = self.template_conn(ip_conn,manufacturer)

               try:

                                primary_ip = (f'{self.ip_conn}/{self.mask}')
                                dev = Device(host=self.ip_conn, user='nocproject', password='h#JN0C8b')
                                dev.open()
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
                                print('this is connect_to_device_juniper_middle!!!!')
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
                                device_type = classifier_device_type(device_type)
                                print('this is connect_to_device_juniper_out!!!!')
                                manufacturer = 'juniper-networks'
                                adding = ADD_NB(device_name, self.site_name, self.location , self.tenants, self.device_role, manufacturer,
                                           self.platform , device_type, primary_ip, interface_name,self.conn_scheme,self.management)
                                adding.add_device()

               except (ConnectAuthError, ConnectClosedError,ConnectError,ConnectTimeoutError):  # exceptions
                    print('\n\n not connect to ' + self.ip_conn + '\n\n')


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
                        device_type = classifier_device_type(re.findall(r'Flex System Fabric EN4093R 10Gb Scalable Switch', output_name_result)[0])
                        interface_name = 'EXTM'
                        manufacturer = 'LENOVO'
                        adding = ADD_NB(device_name, self.site_name,self.location, self.tenants, self.device_role,manufacturer,
                                                   self.platform, device_type, primary_ip, interface_name,self.conn_scheme,self.management)
                        adding.add_device()
            except IndexError as e:
                        print(f"\n\n\n{e}\n\n\n")
            except SSHException as s:
                        print(f"\n\n\n{s}\n\n\n")

if __name__ == '__main__':
     adding = CONNECT_DEVICE()