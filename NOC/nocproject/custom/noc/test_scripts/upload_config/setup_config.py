

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from my_pass import mylogin,mypass
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import yaml
from my_conf import my_config
import datetime


class EXEC_JUNIPER():

    def __init__(self,devices_list=None,config_dict=None):
        self.devices_list = devices_list
        self.config_dict = config_dict

    def juniper_rpc(self,host_ip,dict_config):
        try:
            dev = Device(host=host_ip, user=mylogin, password=mypass)
            dev.open()
            cfg = Config(dev)
            config_list_set = dict_config["config_set"]
            config_list_del = dict_config["config_del"]
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
            with ThreadPoolExecutor(max_workers=30) as executor:
                  result = executor.map(self.juniper_rpc, self.devices_list, repeat(self.config_dict))
        except Exception as err:
            print(f'\n\n{datetime.datetime.now()}\n\n{err}')


if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    executing = EXEC_JUNIPER(devices,my_config)
    executing.exec()
