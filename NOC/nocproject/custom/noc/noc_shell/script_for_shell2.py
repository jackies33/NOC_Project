


from noc.sa.models.managedobject import ManagedObject
from noc.inv.models.interface import Interface
from noc.core.mongo.connection import connect
import csv
connect()

count_mo = 0
count_iface = 0
with open('output_interfaces.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'ip_address', 'interfaces']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for mo in ManagedObject.objects.filter(is_managed=True):
        name = str(mo.name)
        mo_id = mo.id
        ip_address = str(mo.address)
        iface_list = []
        for iface in Interface.objects.filter(managed_object=mo_id):
            iface_name = None
            iface_mac = None
            iface_description = None
            iface_name = str(iface.name)
            iface_mac = str(iface.mac)
            iface_description = str(iface.description)
            iface_list.append({'iface_name':iface_name, 'iface_mac':iface_mac, 'iface_description': iface_description})
            count_iface = count_iface + 1
        writer.writerow({'name':name, 'ip_address':ip_address, 'interfaces':iface_list})
        count_mo = count_mo + 1


