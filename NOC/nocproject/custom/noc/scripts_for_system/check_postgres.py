
'''
for daemon setup script
create  - >> "mcedit /etc/systemd/system/check_postgres.service"
copy in check_postgres.service ->>
_______________________________

[Unit]
Description=Check psql service

[Service]
ExecStart=/usr/bin/python3 /etc/keepalived/check_postgres.py
WorkingDirectory=/etc/keepalived/
Restart=always

[Install]
WantedBy=multi-user.target
_________________________________

<<----check_postgres.service

run next commands -->>>
_____________________________

sudo systemctl daemon-reload
sudo systemctl enable check_postgres.service
sudo systemctl start check_postgres.service

______________________________

<<--- run next commands

'''



import subprocess
import time

status = ''

while True:
    try:

        pg_status = subprocess.run(["systemctl", "is-active", "postgresql@13-main.service"], capture_output=True, text=True).stdout.strip()

        if pg_status == "active":
            if status == "running":
                pass
            elif status == "":
                status = "running"
            elif status == "waiting":
               # subprocess.run("\nsystemctl stop postgresql@13-main\n", shell=True, text=True,capture_output=True)
                subprocess.run(["systemctl", "start", "keepalived"])
                #subprocess.run("\nrm -R /var/lib/postgresql/13/main/pg_replslot/*\n", shell=True, text=True,capture_output=True)
                #subprocess.run("\nsystemctl start postgresql@13-main\n", shell=True, text=True, capture_output=True)
                status = ""

        else:
            if status == "running":
                subprocess.run(["systemctl", "stop", "keepalived"])
                status = "waiting"

            elif status == "waiting":
                pass
        time.sleep(5)
    except Exception as e:
        print(e)
    time.sleep(5)



