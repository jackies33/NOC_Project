

import subprocess
from datetime import datetime
import time
import os

def exec():
    try:
        password = 'noc \n'
        now = datetime.now()
        dt_string = now.strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
        subprocess.run("sudo mount 10.50.100.75:/opt/nfs/noc.tech.mosreg.ru /mnt/sharedfolder_client", shell=True)
        time.sleep(2)
        i = 10
        time.sleep(2)
        subprocess.run(f"sudo PGPASSWORD=noc pg_dump -U noc noc > /mnt/sharedfolder_client/Full/postgresql/noc_backup_{dt_string}.sql",shell=True)
        time.sleep(2)
        filename = f"/mnt/sharedfolder_client/Full/postgresql/noc_backup_{dt_string}.sql"
        while i > 0:
            time.sleep(5)
            i = i - 1
            if os.path.isfile(filename):
                return '1'
            elif i == 0:
                return '0'
    except Exception as e:
        print(e)
        return "0"

if __name__ == '__main__':
    executing = exec()
    print(executing)

