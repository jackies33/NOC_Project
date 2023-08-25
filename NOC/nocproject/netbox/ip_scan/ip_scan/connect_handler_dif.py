

import socket
from .add_device import add_device
from .classifier import classifier_device_type
from .my_pass import mylogin , mypass
from netmiko import ConnectHandler , NetMikoAuthenticationException, NetMikoTimeoutException
import re
from jnpr.junos.exception import ConnectAuthError,ConnectClosedError,ConnectError,ConnectTimeoutError
from jnpr.junos import Device
from lxml import etree



login = mylogin
password = mypass

class conn_device():
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

        def conn_Huawei(self,ip_conn,mask,platform,device_type,site_name,location,device_role,tenants,conn_scheme,management):

               type_device_for_conn = 'huawei'
               host1 = self.template_conn(ip_conn,type_device_for_conn)


               try:

                        with ConnectHandler(**host1) as net_connect:
                                primary_ip = (f'{ip_conn}/{mask}')

                                output_name_result = net_connect.send_command('display current-configuration | include sysname',
                                                                              delay_factor=.5)  # command result
                                device_name = re.findall(r"sysname \S+", output_name_result)[0].split('sysname ')[1]
                                output_version = net_connect.send_command('display version',
                                                                          delay_factor=.5)
                                command_ip = (f'display ip interface brief  | include {ip_conn}')
                                output_ip = net_connect.send_command(command_ip, delay_factor=.5)
                                escaped_ip_address = re.escape(ip_conn)
                                re_ip = (f"(\S+)\s+{escaped_ip_address}")
                                interface_name = re.findall(re_ip, output_ip)[0]
                                device_type = classifier_device_type(re.findall(r'NE20E-S2F|AR6120|NetEngine 8000 F1A-8H20Q', output_version)[0])
                                # print(device_name,device_type,interface_name)
                                net_connect.disconnect()
                                manufacturer = 'huawei-technologies-co'
                                add_device(device_name, site_name,location, tenants, device_role,manufacturer,
                                                           platform, device_type, primary_ip, interface_name,conn_scheme,management)


               except (NetMikoAuthenticationException, NetMikoTimeoutException):  # exceptions
                    print('\n\n not connect to ' + ip_conn + '\n\n')


        def conn_Juniper_rpc(self,ip_conn,mask,platfrom,device_type,site_name,location,device_role,tenants,conn_scheme,management):

               print('this is connect_to_device_juniper!!!!')
               #host1 = self.template_conn(ip_conn,manufacturer)

               try:

                                primary_ip = (f'{ip_conn}/{mask}')
                                dev = Device(host=ip_conn, user='nocproject', password='h#JN0C8b')
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
                                                                    <name>{ip_conn}/{mask}</name>
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
                                add_device(device_name, site_name, location , tenants, device_role, manufacturer,
                                           platfrom , device_type, primary_ip, interface_name,conn_scheme,management)

               except (ConnectAuthError, ConnectClosedError,ConnectError,ConnectTimeoutError):  # exceptions
                    print('\n\n not connect to ' + ip_conn + '\n\n')


if __name__ == '__main__':
     print('main')
