


from concurrent.futures import ThreadPoolExecutor
from my_pass import mylogin,mypass
from itertools import repeat
import logging
from netmiko import ConnectHandler, NetMikoAuthenticationException
import re

class CONNECT_DEVICE():
    """
    Class for connection to different device
    """

    def __init__(self, devices):
        self.devices = devices
        # self.platform = "default"

    def template_conn(self, ip,device_type):
        host1 = ''
        if device_type == 'Huawei Technologies Co.':
            host1 = {

                "host": ip,
                "username": mylogin,
                "password": mypass,
                "device_type": 'huawei',
                "global_delay_factor": 0.5,
            }
        if device_type == 'Juniper Networks':
            host1 = {

                "host": ip,
                "username": mylogin,
                "password": mypass,
                "device_type": 'juniper_junos',
                "global_delay_factor": 0.5,
            }
        return host1


    def send_show(self,device_dict, command):
        ip = device_dict['obj_ip']
        device_type = device_dict['obj_vendor']
        host1 = self.template_conn(ip,device_type)

        try:
            with ConnectHandler(**host1) as ssh:
                result = ssh.send_command(command)
                ssh.disconnect()
            return result
        except NetMikoAuthenticationException as err:
            logging.warning(err)


    def comm_Juniper(self,*args):
        data = []
        command = "show virtual-chassis"
        with ThreadPoolExecutor(max_workers=5) as executor:
            result = executor.map(self.send_show, self.devices, repeat(command))
            for  device , output in zip(self.devices,result):
                find = re.findall(r'\(FPC \d+\)  (?:Prsnt|Mismatch)    \S+', output)
                data2 = []
                data3 = []
                data4 = []
                for target in find:
                    memb = re.findall(r"\(FPC \d+\)", target)[0]
                    member = int(re.findall(r"\d+", memb)[0])
                    if "Mismatch" in target:
                        sn = target.split("Mismatch    ")[1]
                        data3.append({f"Member_id:{member},S/N:{sn}":0})
                    elif "Prsnt" in target:
                        sn = target.split("Prsnt    ")[1]
                        data3.append({f"Member_id:{member},S/N:{sn}":1})
                data4.extend(data3)
                data5 = ({"obj_id":device["obj_id"],
                          "obj_ip":device["obj_ip"],
                          "obj_name":device["obj_name"],
                             "obj_prof_id":device["obj_prof_id"],
                          "obj_vendor":device["obj_vendor"],
                          "obj_vendor_id":device["obj_vendor_id"],
                          "obj_bi_id":device["obj_bi_id"],
                          "obj_target":data4})
                data2.append(data5)
                data.extend(data2)
        return data

