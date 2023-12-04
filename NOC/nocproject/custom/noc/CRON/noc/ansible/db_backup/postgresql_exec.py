

import subprocess
from datetime import datetime
import time

def exec():
    try:
        now = datetime.now()
        dt_string = now.strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
        subprocess.run("sudo mount 10.50.100.75:/opt/nfs/noc.tech.mosreg.ru /mnt/sharedfolder_client", shell=True)
        time.sleep(2)
        subprocess.run(f"sudo -u noc pg_dump noc > /mnt/sharedfolder_client/Full/postgresql/noc_backup_{dt_string}.sql", shell=True)
        return "1"
    except Exception as e:
        return "0"

if __name__ == '__main__':
    executing = exec()
    print(executing)

