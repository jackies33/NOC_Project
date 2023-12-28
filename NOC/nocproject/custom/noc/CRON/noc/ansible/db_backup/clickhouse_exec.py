



import subprocess
import time
from datetime import datetime


def exec():
    try:
        now = datetime.now()
        dt_string = now.strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
        subprocess.run("clickhouse-backup clean", shell=True)
        subprocess.run(f"clickhouse-backup create noc_backup_{dt_string}", shell=True)
        subprocess.run("sudo mount 10.50.100.75:/opt/nfs/noc.tech.mosreg.ru /mnt/sharedfolder_client", shell=True)
        time.sleep(1)
        subprocess.run(f"cp -R /var/lib/clickhouse/backup/noc_backup_{dt_string} /mnt/sharedfolder_client/Full/clickhouse/", shell=True)
        subprocess.run("clickhouse-backup clean", shell=True)
        subprocess.run("rm -R /var/lib/clickhouse/backup/*", shell=True)
        return "1"
    except Exception as e:
        print(e)
        return "0"

if __name__ == '__main__':
    executing = exec()
    print(executing)
