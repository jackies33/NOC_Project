

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from my_pass import my_login,my_pass
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import yaml
from my_conf import my_config_set,my_config_del
import datetime


class EXEC_JUNIPER():

    def __init__(self,devices_list=None,config_list_set=None, config_list_del=None):
        self.devices_list = devices_list
        self.config_list_set = config_list_set
        self.config_list_del = config_list_del

    def juniper_rpc(self,host_ip,config_list_set,config_list_del):
        try:
            dev = Device(host=host_ip, user=my_login, password=my_pass)
            dev.open()
            cfg = Config(dev)
            if config_list_set != []:
                for conf_set in config_list_set:
                      cfg.load(conf_set, format="set")
            else:
                pass
            if config_list_del != []:
                for conf_del in config_list_del:
                      cfg.load(conf_del, format="delete")
            else:
                pass
            cfg.commit(timeout=120)
            dev.close()
            print(f"\n\n<<{host_ip}>> True\n\n")
        except Exception as err:
            print(f'\n\n{datetime.datetime.now()}\n\n{err}')
            print(f"\n\n<<{host_ip}>> False\n\n")


    def exec(self,*args):
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                  result = executor.map(self.juniper_rpc, self.devices_list, repeat(self.config_list_set,self.config_list_del))
        except Exception as err:
            print(f'\n\n{datetime.datetime.now()}\n\n{err}')


if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    executing = EXEC_JUNIPER(devices,my_config_set,my_config_del)
    executing.exec()
