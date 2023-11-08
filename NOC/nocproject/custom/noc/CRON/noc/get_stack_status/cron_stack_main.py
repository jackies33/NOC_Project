
import schedule
import time
from db_exec import PSQL_CONN,MONGO,CH
from conn_dev import CONNECT_DEVICE

''' 
for daemon setup script
create  - >> "mcedit /etc/systemd/system/cron_get_stack.service"
copy in cron_get_stack.service ->> 
_______________________________

[Unit]
Description=Collecting metrics stack status to CH

[Service]
ExecStart=/usr/bin/python3 /opt/cron/noc/get_stack_status/cron_stack_main.py
WorkingDirectory=/opt/cron/noc/get_stack_status/
StandardOutput=file:/var/log/cron_get_stack/output.log
StandardError=file:/var/log/cron_get_stack/error.log
Restart=always

[Install]
WantedBy=multi-user.target
_________________________________

<<----cron_get_stack.service

run next commands -->>>
_____________________________

sudo systemctl daemon-reload
sudo systemctl enable cron_get_stack.service
sudo systemctl start cron_get_stack.service

______________________________

<<--- run next commands

'''


"""
'id' managed_object_profile for get data, if you need to find out the number of id,
execute the next query from postgresql - 'select id,name from sa_managedobjectprofile;'
There you'll need to choose only for check stack status profiles
"""

n = None
profile_list = "'EX3300-48P','EX2200-48P-4G','EX3300-48P'"
my_inventory = []
"'i' - for correct job scheduler. It's need when you start the service , 'my_inventory' is empty yet, and it's nesseccery to fill it " \
"'i' - use here like starting point "
i = 0

class INVENTORY():

    def __init__(self,id_list):
        self.id_list = id_list


    def start_job_inventory(self,*args):
            psql = PSQL_CONN(n, self.id_list)
            id_list = psql.get_id()
            id1 = ''
            for id in id_list:
                id1 = id1 + f"'{id[0]}',"
            id1 = id1.rstrip(",")
            psql = PSQL_CONN(id1, n)
            process = psql.postgre_conn_inv()
            unique_values_id = set([x[-1] for x in process])
            obj_vendor = []
            for value in unique_values_id:
                mongo = MONGO(value)
                obj_vendor.append(mongo.get_vendor())
            global my_inventory
            my_inventory = (self.collect_inv(process, obj_vendor))
            return my_inventory


    def collect_inv(self,inventory,vendor_dict):
            dict_result = []
            for r in inventory:
                dict = {}
                obj_id = r[0]
                obj_name = r[1]
                obj_ip = r[2]
                obj_prof_id = r[3]
                obj_bi_id = r[4]
                obj_vendor_id = r[5]
                for d in vendor_dict:
                    if obj_vendor_id == d['id']:
                        obj_vendor = d['name']
                        dict.update({"obj_id":obj_id,"obj_name":obj_name,"obj_ip":obj_ip,
                                     "obj_prof_id":obj_prof_id,"obj_vendor":obj_vendor,
                                     "obj_vendor_id":obj_vendor_id,"obj_bi_id":obj_bi_id})
                dict_result.append(dict)
            return dict_result


def executer_run():
    dev_exec = CONNECT_DEVICE(my_inventory)
    for m in my_inventory:
        obj_vendor = m['obj_vendor']
        if obj_vendor == "Juniper Networks":
            my_list = dev_exec.comm_Juniper()
            ch = CH(my_list)
            result = ch.ch_insert()
        if obj_vendor == "Huawei Technologies Co.":
            my_list = ''


int = INVENTORY(profile_list)
schedule.every(5).minutes.do(executer_run)
schedule.every(24).hours.do(int.start_job_inventory)

while i == 0:
    my_inventory = int.start_job_inventory(profile_list)
    time.sleep(1)
    i = i+1
while i == 1:
    schedule.run_pending()
    time.sleep(1)
