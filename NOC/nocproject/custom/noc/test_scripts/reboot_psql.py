

import time
import os
import psycopg2

'''
for daemon setup script
create  - >> "mcedit etc/systemd/system/reboot_psql.service"
copy in reboot_psql.service ->>
_______________________________

[Unit]
Description=Reboot psql service

[Service]
ExecStart=/usr/bin/python3.9 /opt/custom/rebpsql.py
StandardOutput=file:/var/log/reboot_psql/output.log
StandardError=file:/var/log/reboot_psql/error.log
Restart=always

[Install]
WantedBy=multi-user.target
_________________________________

<<----copy in reboot_psql.service

run next commands -->>>
_____________________________
sudo systemctl daemon-reload
sudo systemctl enable reboot_psql.service
sudo systemctl start reboot_psql.service

______________________________

<<--- run next commands

'''



while True:
    conn = psycopg2.connect(database="noc", user="noc", password="noc", host="10.50.50.170", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle';")
    conn.commit()
    conn.close()
    time.sleep(1800)


#while True:
#   os.system('systemctl restart postgresql@14-main.service')
#   time.sleep(10800)
