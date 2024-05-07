


from datetime import datetime
import subprocess
import time
import os

def exec():
    try:
        now = datetime.now()
        dt_string = now.strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
        subprocess.run("rm -R /tmp/mongo_db_bp/*", shell=True)
        subprocess.run("mongodump -u noc -p noc --db noc --out /tmp/mongo_db_bp/", shell=True)
        subprocess.run("sudo mount 10.50.100.75:/opt/nfs/noc.tech.mosreg.ru /mnt/sharedfolder_client", shell=True)
        time.sleep(10)
        i = 10
        subprocess.run(f"mkdir /mnt/sharedfolder_client/Full/mongodb/noc_backup_{dt_string}", shell=True)
        time.sleep(10)
        subprocess.run(f"cp -R /tmp/mongo_db_bp/noc/ /mnt/sharedfolder_client/Full/mongodb/noc_backup_{dt_string}/noc/", shell=True)
        time.sleep(10)
        dir = f"/mnt/sharedfolder_client/Full/mongodb/noc_backup_{dt_string}"
        while i > 0:
            time.sleep(10)
            i = i - 1
            if os.path.isdir(dir):
                return '1'
            elif i == 0:
                return '0'
    except Exception as e:
        print(f"Error: \n {e} \n")
        result = "0"
        return result

if __name__ == '__main__':
    executing = exec()
    print(executing)


