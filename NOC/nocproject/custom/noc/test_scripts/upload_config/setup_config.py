

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from my_pass import my_login,my_pass
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import yaml
from my_conf import my_config
import datetime


class EXEC_JUNIPER():

    def __init__(self,devices_list=None,config_list=None):
        self.devices_list = devices_list
        self.config_list = config_list

    def juniper_rpc(self,host_ip,config_list):
        try:
            dev = Device(host=host_ip, user=my_login, password=my_pass)
            dev.open()
            cfg = Config(dev)
            for conf in config_list:
                  cfg.load(conf, format="set")
            cfg.commit(timeout=120)
            dev.close()
            print(f"\n\n<<{host_ip}>> True\n\n")
        except Exception as err:
            print(f'\n\n{datetime.datetime.now()}\n\n{err}')
            print(f"\n\n<<{host_ip}>> False\n\n")


    def exec(self,*args):
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                  result = executor.map(self.juniper_rpc, self.devices_list, repeat(self.config_list))
        except Exception as err:
            print(f'\n\n{datetime.datetime.now()}\n\n{err}')


if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    executing = EXEC_JUNIPER(devices,my_config)
    executing.exec()
