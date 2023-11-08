


import subprocess
import schedule
import time
import  logging
from datetime import datetime
from pytz import timezone



''' 
for daemon setup script
create  - >> "mcedit /etc/systemd/system/cron_ansible_lbreset.service"
copy in cron_ansible_lbreset.service ->> 
_______________________________

[Unit]
Description=Execute ansible tasks for one time in 4 days for liftbridge migration(For correct job liftbridge and all of services in NOC)

[Service]
ExecStart=/usr/bin/python3 /opt/ansible/lbreset/scheduler.py
WorkingDirectory=/opt/ansible/lbreset/
StandardError=file:/var/log/ansible/lbreset/scheduler_error.log
Restart=always

[Install]
WantedBy=multi-user.target
_________________________________

<<----cron_ansible_lbreset.service

run next commands -->>>
_____________________________

sudo systemctl daemon-reload
sudo systemctl enable cron_ansible_lbreset.service
sudo systemctl cron_ansible_lbreset.service

______________________________

<<--- run next commands

'''


def run_playbook():
    cmd = "ansible-playbook /opt/ansible/lbreset/playbook.yml"
    logging.basicConfig(filename='/var/log/ansible/lbreset/output.log', level=logging.DEBUG)
    tz = timezone('Europe/Moscow')
    timenow = datetime.now(tz).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    time.sleep(10)
    logging.info(f"\n\n\n{timenow} - 'Ansible Output': {result.stdout}\n\n\n")

schedule.every(4).days.do(run_playbook)

while True:
    schedule.run_pending()
    time.sleep(1)


