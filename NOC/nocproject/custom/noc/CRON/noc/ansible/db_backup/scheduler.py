

import subprocess
import  logging
import datetime
from pytz import timezone
import time



''' 
for daemon setup script
create  - >> "mcedit /etc/systemd/system/cron_ansible_backup_db.service"
copy in cron_ansible_backup_db.service ->> 
_______________________________

[Unit]
Description=Execute ansible playbooks for automate backup for DB's

[Service]
ExecStart=/usr/bin/python3 /opt/ansible/db_backup/scheduler.py
WorkingDirectory=/opt/ansible/db_backup/
Restart=always

[Install]
WantedBy=multi-user.target
_________________________________

<<----cron_ansible_backup_db.service

run next commands -->>>
_____________________________

sudo systemctl daemon-reload
sudo systemctl enable cron_ansible_backup_db.service
sudo systemctl start cron_ansible_backup_db.service

______________________________

<<--- run next commands

'''


i = 0

def run_playbook():
    cmd_mongo = "ansible-playbook /opt/ansible/db_backup/run_mongo.yml"
    cmd_pgsql = "ansible-playbook /opt/ansible/db_backup/run_pgsql.yml"
    cmd_pgsql_netbox = "ansible-playbook /opt/ansible/db_backup/run_pgsql_netbox.yml"
    #cmd_clickhouse = "ansible-playbook /opt/ansible/db_backup/run_clickhouse.yml"
    logging.basicConfig(filename='/var/log/ansible/db_backup/output.log', level=logging.DEBUG)
    tz = timezone('Europe/Moscow')
    timenow = datetime.datetime.now(tz).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    result_mongo = subprocess.run(cmd_mongo, shell=True, capture_output=True, text=True)
    result_pgsql = subprocess.run(cmd_pgsql, shell=True, capture_output=True, text=True)
    result_pgsql_netbox =subprocess.run(cmd_pgsql_netbox, shell=True, capture_output=True, text=True)
    #result_clickhouse = subprocess.run(cmd_clickhouse, shell=True, capture_output=True, text=True)
    time.sleep(10)
    logging.info(f"\n\n\n{timenow} - 'Ansible Output MONGO': {result_mongo.stdout}\n\n\n")
    logging.info(f"\n\n\n{timenow} - 'Ansible Output POSTGRESQL': {result_pgsql.stdout}\n\n\n")
    logging.info(f"\n\n\n{timenow} - 'Ansible Output POSTGRESQL_NETBOX': {result_pgsql_netbox.stdout}\n\n\n")
    #logging.info(f"\n\n\n{timenow} - 'Ansible Output CLLICKHOUSE': {result_clickhouse.stdout}\n\n\n")

run_time = datetime.time(hour=23, minute=55, second=0)

while i == 0:
    run_playbook()
    i = 1

while i == 1:
    now = datetime.datetime.now()
    if now.weekday() == 6 and now.time() >= run_time:
        run_playbook()
        time.sleep(7200) #sleep for waiting other day, and don't let to make job again in the same day
    else:
        time.sleep(120) # enough time for request , and also not so often




