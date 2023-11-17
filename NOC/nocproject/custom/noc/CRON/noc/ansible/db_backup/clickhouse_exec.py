



import subprocess
from datetime import datetime


def exec():
    try:
        now = datetime.now()
        dt_string = now.strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
        subprocess.run("clickhouse-backup create", shell=True)
        subprocess.run(f"mkdir /mnt/sharedfolder_client/Full/clickhouse/noc_backup_{dt_string}", shell=True)
        subprocess.run(f"cp -R /var/lib/clickhouse/shadow/ /mnt/sharedfolder_client/Full/clickhouse/noc_backup_{dt_string}/", shell=True)
        subprocess.run("rm -R /var/lib/clickhouse/shadow/*", shell=True)
        subprocess.run("rm -R /var/lib/clickhouse/store/backup/*", shell=True)
        return "1"
    except Exception as e:
        return "0"

if __name__ == '__main__':
    executing = exec()
    print(executing)
