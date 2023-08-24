


import traceback
import time
import pynetbox
from .tgbot import tg_bot
import datetime

"""
#name='klin-ar01'
#site=6
#tenants=2
#device_role = 2
#manufacturer = "Huawei"
#device_type = 3
#primary_ip = '10.100.138.37/32'
#tags=['primary_ip']
#interface_name = "Loopback1"
"""

status = 'active'
type_of_interface = 'virtual'
aobjt = 'dcim.interface'



def add_device(name , site , location, tenants , device_role , manufacturer ,platform, device_type ,
               primary_ip , interface_name ,conn_scheme, management):
    print('this is add_device.py!!!!')
    print(site)
    #print (status , str(name),str(primary_ip),int(site[1]),int(device_role[0]),int(device_type),int(tenants[0]))

    nb = pynetbox.api(url='https://10.50.64.71',
                      token='3f6382e7f9c312ecc8cc2eca9f70293b5ca7edaa')
    nb.http_session.verify = False

    try:
        nb.dcim.devices.create(
               name=name,
               status = str(management[1]).lower(),
               site=site[1],
               location=location[0],
               device_role=device_role[0],
               manufacturer=manufacturer[1].title(),
               platform=platform[0],
               device_type = device_type,
               primary_ip = primary_ip,
               tenant = tenants[0],
               custom_fields = {'Connection_scheme': conn_scheme},
        )

    except pynetbox.core.query.RequestError:
               print(f'device {name} is already done or \n')
               print('Error:\n', traceback.format_exc())

    time.sleep(1)
    id_device = nb.dcim.devices.get(name=name)
    print(id_device.id)
    try:
        create = nb.dcim.interfaces.create(
            device= id_device.id,
            name=interface_name,
            type=type_of_interface,
            enabled=True,
    )
    except pynetbox.core.query.RequestError:
            print(f'interface {interface_name} is already done')

    time.sleep(1)
    interface = nb.dcim.interfaces.get(name=interface_name, device_id=id_device.id)
    interface_id = interface['id']

    try:
               ip_address = nb.ipam.ip_addresses.create(
               address=primary_ip,
               status=status,
               assigned_object_type=aobjt,
               assigned_object_id=interface_id,
               )

    except TypeError:
        print('Error for create an ip_address')
        return False
    time.sleep(1)

    try:
        id_device.update({'primary_ip4': {'address': primary_ip}})
    except pynetbox.core.query.RequestError:
        print(f"ip_address {primary_ip} is already done")
    else:
        print(f"Succesfull create and update device - {name} and send to telegram chat")
        message = (f'Netbox.handler[Event_Add Device]\n Device Name - [ {name} ] \n ip_address - [{primary_ip}] \n Time: {datetime.datetime.now()}')
        tg_bot.tg_sender(message)

if __name__ == '__main__':
     add_device()


