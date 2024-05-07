


from noc.sa.models.managedobject import ManagedObject
from noc.inv.models.interface import Interface
from noc.core.mongo.connection import connect
import csv
connect()

count_mo = 0
count_iface = 0
with open('output_all_managed_objects.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'ip_address', 'description', 'tags',
                  'mo_profile', 'sa_profile', 'platform', 'adm_dom', 'segment','pool', 'interfaces']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    iface_list = []
    for mo in ManagedObject.objects.filter(is_managed=True):
        name = str(mo.name)
        mo_id = mo.id
        ip_address = str(mo.address)
        description = str(mo.description)
        tags = str(mo.tags)
        mo_profile = str(mo.object_profile)
        sa_profile = str(mo.profile)
        platform = str(mo.platform)
        adm_dom = str(mo.administrative_domain)
        segment = str(mo.segment)
        pool = str(mo.pool)
        for iface in Interface.objects.filter(managed_object=mo_id):
            iface_name = None
            iface_mac = None
            iface_description = None
            iface_name = str(iface.name)
            iface_mac = str(iface.mac)
            iface_description = str(iface.description)
            iface_list.append({'iface_name':iface_name, 'iface_mac':iface_mac, 'iface_description': iface_description})
            count_iface = count_iface + 1
        writer.writerow({'name':name, 'ip_address':ip_address, 'description':description, 'tags':tags,
                  'mo_profile':mo_profile, 'sa_profile':sa_profile, 'platform':platform,
                         'adm_dom':adm_dom, 'segment':segment,'pool':pool, 'interfaces':iface_list})
        count_mo = count_mo + 1


    #if config != []:
     #     count = count + 1
          #data = config.encode()
          #config = zlib.compress(data)
          #writer.writerow({'Name': name, 'IP Address': ip_address, 'Config': config})

