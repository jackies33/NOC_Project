

'''
for daemon setup script
create  - >> "mcedit /etc/systemd/system/check_clickhouse.service"
copy in check_clickhouse.service ->>
_______________________________

[Unit]
Description=Check clickhouse service

[Service]
ExecStart=/usr/bin/python3 /etc/keepalived/check_clickhouse.py
WorkingDirectory=/etc/keepalived/
Restart=always

[Install]
WantedBy=multi-user.target
_________________________________

<<----check_clickhouse.service

run next commands -->>>
_____________________________

sudo systemctl daemon-reload
sudo systemctl enable check_clickhouse.service
sudo systemctl start check_clickhouse.service

______________________________

<<--- run next commands

'''



import subprocess
import time

status = ''

while True:
    pg_status = subprocess.run(["systemctl", "is-active", "clickhouse-server.service"], capture_output=True, text=True).stdout.strip()

    if pg_status == "active":
        if status == "running":
            pass
        elif status == "":
            status = "running"
        elif status == "waiting":
            subprocess.run(["systemctl", "start", "keepalived"])
            subprocess.run(["systemctl", "start", "haproxy"])
            status = ""

    else:
        if status == "running":
            subprocess.run(["systemctl", "stop", "keepalived"])
            subprocess.run(["systemctl", "stop", "haproxy"])
            status = "waiting"
        elif status == "waiting":
            pass
    time.sleep(5)



