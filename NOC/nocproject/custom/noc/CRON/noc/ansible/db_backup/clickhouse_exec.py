



import subprocess
import time
from datetime import datetime
import os


def exec():
    try:
        now = datetime.now()
        dt_string = now.strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
        subprocess.run("clickhouse-backup clean", shell=True)
        subprocess.run(f"clickhouse-backup create noc_backup_{dt_string}", shell=True)
        time.sleep(5)
        subprocess.run("sudo mount 10.50.100.75:/opt/nfs/noc.tech.mosreg.ru /mnt/sharedfolder_client", shell=True)
        time.sleep(5)
        i = 10
        subprocess.run(f"cp -R /var/lib/clickhouse/backup/noc_backup_{dt_string} /mnt/sharedfolder_client/Full/clickhouse/", shell=True)
        time.sleep(5)
        subprocess.run("clickhouse-backup clean", shell=True)
        time.sleep(5)
        subprocess.run("rm -R /var/lib/clickhouse/backup/*", shell=True)
        time.sleep(5)
        return '1'
        #dir = f"/mnt/sharedfolder_client/Full/clickhouse/noc_backup_{dt_string}"
        #while i > 0:
        #    time.sleep(120)
        #    i = i - 1
        #    if os.path.isdir(dir):
         #       return '1'
         #   elif i == 0:
         #       return '0'
    except Exception as e:
        print(e)
        return "0"

if __name__ == '__main__':
    executing = exec()
    print(executing)
