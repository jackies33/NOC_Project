


'''
for daemon setup script
create  - >> "mcedit /etc/systemd/system/check_ip_for_db.service"
copy in check_ip_for_db.service ->>
_______________________________

[Unit]
Description=Check ip for db service

[Service]
ExecStart=/usr/bin/python3 /etc/keepalived/check_ip_for_db.py
WorkingDirectory=/etc/keepalived/
Restart=always

[Install]
WantedBy=multi-user.target
_________________________________

<<----check_postgres.service

run next commands -->>>
_____________________________

sudo systemctl daemon-reload
sudo systemctl enable check_ip_for_db.service
sudo systemctl start check_ip_for_db.service

______________________________

<<--- run next commands

'''


import time
import subprocess
import pexpect
from datetime import datetime

password = "P@ssw0rd"

i = 0
while True:

    try:

        checking = subprocess.run("\nip a | grep '10.50.50.170'\n", shell=True,text=True,capture_output=True)
        output = str(checking.stdout.strip())
        if output == 'inet 10.50.50.170/24 scope global ens192.vmac' and i == 0:
            subprocess.run("\nrm -R /var/lib/postgresql/13/main/standby.signal\n", shell=True,text=True,capture_output=True)
            subprocess.run("\nsudo systemctl restart postgresql@13-main\n", shell=True, text=True, capture_output=True)
            i = 2
            pass
        elif output == 'inet 10.50.50.170/24 scope global ens192.vmac' and i == 1:
            subprocess.run("\nrm -R /var/lib/postgresql/13/main/standby.signal\n", shell=True,text=True,capture_output=True)
            subprocess.run("\nsudo systemctl restart postgresql@13-main\n", shell=True, text=True, capture_output=True)
            i = 2
            pass
        elif output == '' and i == 2:
            now = datetime.now()
            dt_string = now.strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
            #subprocess.run("sudo mount 10.50.100.75:/opt/nfs/zabbix.tech.mosreg.ru /mnt/sharedfolder_client", shell=True)
            #subprocess.run(f"sudo PGPASSWORD=zabbix pg_dump -U zabix zabbix > /mnt/sharedfolder_client/Full/postgresql/zabbix_backup_{dt_string}.sql",shell=True)
            subprocess.run(f"sudo PGPASSWORD=zabbix pg_dump -U zabix zabbix > /var/lib/postgresql/13/backup/zabbix_backup_{dt_string}.sql",shell=True)
            #subprocess.run("\n rm -R /var/lib/postgresql/13/main/* \n", shell=True,text=True,capture_output=True)
            #child = pexpect.spawn("sudo pg_basebackup -h 10.50.50.171 -U replication -X stream -C -S replica_1 -v -R -D /var/lib/postgresql/13/main/")
            #child.expect("Password:")
            #child.sendline("P@ssw0rd")
            #child.read().decode('utf-8')
            #subprocess.run("\nsudo chown -R postgres:postgres /var/lib/postgresql/13/main\n", shell=True, text=True,capture_output=True)
            #subprocess.run("\nsudo chmod -R 700 /var/lib/postgresql/13/main\n", shell=True, text=True,capture_output=True)
            #subprocess.run("\nsudo systemctl restart postgresql@13-main\n", shell=True, text=True, capture_output=True)
            i = 1
            pass
        elif output == '' and i == 1:
            pass
        elif output == '' and i == 0:
            i = 1
            pass


        time.sleep(5)
    except Exception as e:
        print(e)
    time.sleep(5)



