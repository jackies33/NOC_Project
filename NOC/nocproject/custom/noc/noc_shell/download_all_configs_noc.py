



from noc.sa.models.managedobject import ManagedObject
from noc.core.mongo.connection import connect
connect()
import csv

count = 0
my_list = []
with open('output_all_configs.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name', 'IP Address', 'Config']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for mo in ManagedObject.objects.filter(is_managed=True):
        name = mo.name
        ip_address = mo.address
        config = str(mo.config.read())
        if config != []:
              count = count + 1
              #data = config.encode()
              #config = zlib.compress(data)
              writer.writerow({'Name': name, 'IP Address': ip_address, 'Config': config})







