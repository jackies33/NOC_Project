

'''
for daemon setup script
create  - >> "mcedit /etc/systemd/system/check_nginx.service"
copy in check_nginx.service ->>
_______________________________

[Unit]
Description=Check nginx service

[Service]
ExecStart=/usr/bin/python3 /etc/keepalived/check_nginx.py
WorkingDirectory=/etc/keepalived/
Restart=always

[Install]
WantedBy=multi-user.target
_________________________________

<<----check_nginx.service

run next commands -->>>
_____________________________

sudo systemctl daemon-reload
sudo systemctl enable check_nginx.service
sudo systemctl start check_nginx.service

______________________________

<<--- run next commands

'''



import subprocess
import time

status = ''

while True:
    try:
        pg_status = subprocess.run(["systemctl", "is-active", "nginx.service"], capture_output=True, text=True).stdout.strip()

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
    except Exception as e:
        print(e)

    time.sleep(5)



