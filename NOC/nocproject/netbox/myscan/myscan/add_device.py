
import traceback
import time
import pynetbox
from .tgbot import tg_bot
import datetime
from .my_pass import netbox_url,netbox_api_token

class ADD_NB():

        """
        class for add data to NetBox over RestApi
        """

        def __init__(self, name_device, site, location, tenants, device_role,
                     manufacturer,platform, device_type,
                       primary_ip, interface_name,conn_scheme, management):

            self.status = 'active'
            self.type_of_interface = 'virtual'
            self.aobjt = 'dcim.interface'
            self.name_device = name_device
            self.site = site
            self.location =location
            self.tenants = tenants
            self.device_role = device_role
            self.manufacturer = manufacturer
            self.platform = platform
            self.device_type = device_type
            self.primary_ip = primary_ip
            self.interface_name = interface_name
            self.conn_scheme = conn_scheme
            self.management = management

        def add_device(self,*args):
           # print('this is add_device.py!!!!')

            # conn_scheme,str(management[1].lower))
            if self.management == 1:
                self.management = "Active"
            elif self.management == 2:
                self.management = "Offline"
            nb = pynetbox.api(url=netbox_url,
                              token=netbox_api_token)
            nb.http_session.verify = False
            site = self.site[0]
            #print(self.name_device, site, self.location, self.tenants, self.device_role,
                 # self.manufacturer, self.platform, self.device_type,
                 # self.primary_ip, self.interface_name, self.conn_scheme, self.management)
            try:
                nb.dcim.devices.create(
                       name=self.name_device,
                       status = str(self.management).lower(),
                       site=site[1],
                       location=self.location,
                       device_role=self.device_role,
                       manufacturer=self.manufacturer.title(),
                       platform=self.platform[0],
                       device_type = self.device_type,
                       primary_ip = self.primary_ip,
                       tenant = self.tenants,
                       custom_fields = {'Connection_Scheme': str(self.conn_scheme)},
                )

            except pynetbox.core.query.RequestError:
                       print(f'device {self.name_device} is already done or \n')
                       print('Error:\n', traceback.format_exc())

            time.sleep(1)
            id_device = nb.dcim.devices.get(name=self.name_device)
            try:
                create = nb.dcim.interfaces.create(
                    device= id_device.id,
                    name=self.interface_name,
                    type=self.type_of_interface,
                    enabled=True,
            )
            except pynetbox.core.query.RequestError:
                    print(f'interface {self.interface_name} is already done')

            time.sleep(1)
            interface = nb.dcim.interfaces.get(name=self.interface_name, device_id=id_device.id)
            interface_id = interface['id']

            try:
                       ip_address = nb.ipam.ip_addresses.create(
                       address=self.primary_ip,
                       status=self.status,
                       assigned_object_type=self.aobjt,
                       assigned_object_id=interface_id,
                       )

            except TypeError:
                print('Error for create an ip_address')
                return False
            time.sleep(1)

            try:
                id_device.update({'primary_ip4': {'address': self.primary_ip}})
            except pynetbox.core.query.RequestError:
                print(f"ip_address {self.primary_ip} is already done")
            else:
                print(f"Succesfull create and update device - {self.name_device} and send to telegram chat")
                message = (f'Netbox.handler[Event_Add Device]\n Device Name - [ {self.name_device} ] '
                           f'\n ip_address - [{self.primary_ip}] \n Time: {datetime.datetime.now()}')
                sender = tg_bot(message)
                sender.tg_sender()

if __name__ == '__main__':
    print("__main__")


